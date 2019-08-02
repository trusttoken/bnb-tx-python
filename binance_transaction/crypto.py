from ecdsa import VerifyingKey
from ecdsa.curves import SECP256k1
from ecdsa.keys import BadSignatureError

"""
crypto.py

Utilities for discrete mathematics and cryptography
"""


def pow_mod(x, y, z):
    "Calculate (x ** y) % z efficiently."
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
    return number


def int_to_bytes(x, length=False):
    return x.to_bytes(length or (x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')


secp256k1 = {
    "prime": 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    "base": 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    "name": 'secp256k1',
}


def uncompress_key(compressed_key, prime=secp256k1['prime']):
    assert len(compressed_key) == 33
    y_parity = int_from_bytes(compressed_key[:1]) - 2
    x = int_from_bytes(compressed_key[1:])
    a = (pow_mod(x, 3, prime) + 7) % prime
    y = pow_mod(a, (prime+1)//4, prime)
    if y % 2 != y_parity:
        y = -y % prime
    return b'\x04' + int_to_bytes(x, 32) + int_to_bytes(y, 32)


def compress_key(uncompressed_key):
    assert len(uncompressed_key) == 65
    assert uncompressed_key[0:1] == b'\x04'
    y_odd = int_from_bytes(uncompressed_key[33:]) % 2
    return int_to_bytes(y_odd + 2, 1) + uncompressed_key[1:33]


def verify_sig(uncompressed_public_key, digest, signature, curve=SECP256k1):
    assert len(uncompressed_public_key) == 65
    vk = VerifyingKey.from_string(uncompressed_public_key[1:], curve=curve)
    try:
        return vk.verify_digest(signature, digest)
    except BadSignatureError:
        return False
