"""
bech32.py

Pronounced BAYCH THIRTY TWO
bech32 address encoding
begins with a human readable prefix (hrp)
ends with a checksum
"""


# Modified from the reference implementation: https://github.com/sipa/bech32/blob/master/ref/python/segwit_addr.py

BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def bech32_polymod(values):
    """Internal function that computes the Bech32 checksum."""
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ value
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0
    return chk


def bech32_hrp_expand(hrp):
    """Expand the HRP into values for checksum computation."""
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_verify_checksum(hrp, data):
    """Verify a checksum given HRP and converted data characters."""
    return bech32_polymod(bech32_hrp_expand(hrp) + data) == 1


def bech32_create_checksum(hrp, data):
    """Compute the checksum values given HRP and data."""
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def bech32_encode_raw(hrp, data):
    """Compute a Bech32 string given HRP and data values."""
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + '1' + ''.join([BECH32_CHARSET[d] for d in combined])


def bech32_decode_raw(bech):
    """Validate a Bech32 string, and determine HRP and data."""
    if ((any(ord(x) < 33 or ord(x) > 126 for x in bech)) or
            (bech.lower() != bech and bech.upper() != bech)):
        print('invalid: out of range')
        return (None, None)
    bech = bech.lower()
    pos = bech.rfind('1')
    if pos < 1 or pos + 7 > len(bech) or len(bech) > 90:
        print('invalid: wrongly positioned 1')
        return (None, None)
    if not all(x in BECH32_CHARSET for x in bech[pos+1:]):
        print('invalid: not all in charset')
        return (None, None)
    hrp = bech[:pos]
    data = [BECH32_CHARSET.find(x) for x in bech[pos+1:]]
    if not bech32_verify_checksum(hrp, data):
        print('invalid: checksum')
        return (None, None)
    return (hrp, data[:-6])


def convertbits(data, frombits, tobits, pad=True):
    """General power-of-2 base conversion."""
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret


def bech32_decode(hrpexpected, addr):
    """Decode a bech32 address."""
    hrpgot, data = bech32_decode_raw(addr)
    if hrpgot != hrpexpected:
        print('invalid: %s != %s' % (hrpgot, hrpexpected))
        return (None, None)
    decoded = convertbits(data, 5, 8, False)
    if decoded is None or len(decoded) < 2 or len(decoded) > 40:
        print('invalid decoded: %s' % decoded)
        return (None, None)
    return decoded


def bech32_encode(hrp, data):
    """Encode a bech32 address."""
    ret = bech32_encode_raw(hrp, convertbits(data, 8, 5))
    if bech32_decode(hrp, ret) == (None, None):
        return None
    return ret


def address_bytes(address_str):
    hrp, raw_bech32 = bech32_decode_raw(address_str)
    return bytes(convertbits(raw_bech32, 5, 8, False))
