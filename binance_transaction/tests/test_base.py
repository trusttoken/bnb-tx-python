from binance_transaction.base import Bool, Bytes, String, StringVarInt, VarInt


import base64


def test_decode_varint():
    for val in [5, 257, 1000000, 0]:
        encoded = VarInt(val).encode()
        decoded, remaining = VarInt.decode(encoded)
        assert decoded == val
        assert remaining == b''


def test_decode_strvarint():
    for val in ['5', '257', '1000000', '0']:
        encoded = StringVarInt(val).encode()
        decoded, remaining = StringVarInt.decode(encoded)
        assert decoded == val
        assert remaining == b''


def test_decode_str():
    for val in ["", "TrueUSD"]:
        encoded = String(val).encode()
        decoded, remaining = String.decode(encoded)
        assert decoded == val
        assert remaining == b''


def test_decode_bool():
    for val in [True, False]:
        encoded = Bool(val).encode()
        decoded, remaining = Bool.decode(encoded)
        assert decoded == val
        assert remaining == b''


def test_decode_bytes():
    for val in [b'', b'0', b'1', b'1000']:
        b64val = base64.b64encode(val).decode('utf8')
        encoded = Bytes(b64val).encode()
        decoded, remaining = Bytes.decode(encoded)
        assert decoded == b64val
        assert remaining == b''
