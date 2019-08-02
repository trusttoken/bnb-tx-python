import base64

from binance_transaction.bech32 import bech32_encode, address_bytes


"""
base.py

Base components for transaction encoding
Includes amino and its primitive types

* Amino
* make_prefix
* VarInt
* Bool
* Repeated
* RepeatedPacked
* String
* StringVarInt
* Bytes
* Address
* Token
* StringToken
* Input
* Output
"""


class Amino(dict):
    def encode(self, field_id=None):
        raise NotImplementedError

    @staticmethod
    def decode(data, field_id=None):
        raise NotImplementedError


def make_prefix(field_id, type_id):
    return VarInt(field_id << 3 | type_id).encode()


class VarInt(int):
    def __new__(cls, val):
        return super(VarInt, cls).__new__(cls, val)

    def encode(self, field_id=None):
        # https://developers.google.com/protocol-buffers/docs/encoding
        # base 128
        int_bytes = []
        remaining = int(self)
        if remaining == 0:
            return b''
        while remaining >= 128:
            int_bytes.append(remaining % 128 + 128)
            remaining //= 128
        int_bytes.append(remaining)
        if field_id is None:
            return bytes(int_bytes)
        else:
            return make_prefix(field_id, 0) + bytes(int_bytes)

    @staticmethod
    def decode(data, field_id=None):
        if field_id is not None:
            prefix = make_prefix(field_id, 0)
            for i in range(len(prefix)):
                if prefix[i] != data[i]:
                    return VarInt(0), data
            data = data[len(prefix):]
        amount = 0
        if len(data) == 0:
            return VarInt(0), data
        mul = 1
        for i in range(len(data)):
            amount += (data[i] % 128) * mul
            if data[i] < 128:
                return VarInt(amount), data[i+1:]
            mul *= 128
        assert False, 'Reached end while parsing VarInt from %s' % data


class Bool(VarInt):
    """
    This would subclass bool if that were possible :(
    We cannot make json.dumps print true or false otherwise so we unwrap for that
    This class still helps with encoding and decoding.
    https://github.com/python/cpython/blob/master/Lib/json/encoder.py#L305
    """
    def __new__(cls, val):
        return super(Bool, cls).__new__(cls, 1 if val else 0)

    @staticmethod
    def decode(data, field_id=None):
        if field_id is not None:
            for i in range(len(field_id)):
                if field_id[i] != data[i]:
                    return Bool(False), data
            data = data[len(field_id):]
        if len(data) == 0:
            return Bool(False), data
        return Bool(data[0]), data[1:]


class Repeated(list):
    def __new__(cls, values):
        return super(Repeated, cls).__new__(cls, values)

    def encode(self, field_id):
        buf = b''
        for amino_value in self:
            buf += amino_value.encode(field_id)
        return buf

    @staticmethod
    def decode(data, prefix, klass=None):
        items = []
        while True:
            for i in range(len(prefix)):
                if data[i] != prefix[i]:
                    return Repeated(items), data
            item, data = klass.decode(data, prefix)
            items.append(item)


class RepeatedPacked(list):
    """
    Warning: This class is not used nor tested, but remains to help with future encoding
    """
    def __new__(cls, values):
        return super(RepeatedPacked, cls).__new__(cls, values)

    def encode(self, field_id):
        buf = b''
        for amino_value in self:
            buf += amino_value.encode()
        return make_prefix(field_id, 0) + buf


class String(str):
    def __new__(cls, data):
        if data is None:
            return String.__new__(cls, '')
        return super(String, cls).__new__(cls, data)

    def encode(self, field_id=None):
        if self is None or len(self) == 0:
            return b''
        buf = VarInt(len(self)).encode() + str.encode(self, 'utf8')
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + buf

    @staticmethod
    def decode(data, field_id=None):
        if field_id is not None:
            for i in range(len(field_id)):
                if field_id[i] != data[i]:
                    return String(''), data
            data = data[len(field_id):]
        length, data = VarInt.decode(data)
        return String(data[0:length].decode('utf8')), data[length:]


class StringVarInt(String):
    """
    A numeric string for JSON, but a VarInt when amino-encoded
    Invented by Binance Engineering to confuse engineers
    """
    def encode(self, field_id=None):
        return VarInt.encode(int(self), field_id)

    def decode(data, field_id=None):
        varint, data = VarInt.decode(data, field_id)
        return StringVarInt(str(varint)), data


# json as base64 string
class Bytes(String):
    def encode(self, field_id=None):
        if self is None or len(self) == 0:
            return b''
        buf = base64.b64decode(str(self))
        buf = VarInt(len(buf)).encode() + buf
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + buf

    @staticmethod
    def decode(data, field_id=None):
        if field_id is not None:
            prefix = make_prefix(field_id, 2)
            for i in range(len(prefix)):
                if prefix[i] != data[i]:
                    return Bytes(''), data
            data = data[len(prefix):]
        length, data = VarInt.decode(data)
        return Bytes(base64.b64encode(data[0:length]).decode('utf8')), data[length:]


# json as bnb1 address
class Address(String):
    def encode(self, field_id=None):
        if len(self) == 0:
            return b''
        buf = VarInt(20).encode() + address_bytes(self)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + buf

    @staticmethod
    def decode(data, field_id=None, hrp='bnb'):
        if field_id is not None:
            prefix = make_prefix(field_id, 2)
            for i in range(len(prefix)):
                if prefix[i] != data[i]:
                    return Address(''), data
            data = data[len(prefix):]
        length, data = VarInt.decode(data)
        return Address(bech32_encode(hrp, data[0:length])), data[length:]


class Token(Amino):
    def __init__(self, amount, denom):
        dict.__init__(self, amount=VarInt(amount), denom=denom)

    def encode(self, field_id=None):
        buf = String(self['denom']).encode(1)
        buf += VarInt(self['amount']).encode(2)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    @staticmethod
    def decode(data, field_id=None):
        if field_id is not None:
            prefix = make_prefix(field_id, 2)
            for i in range(len(prefix)):
                if prefix[i] != data[i]:
                    return Address(''), data
            data = data[len(field_id):]
        denom, data = String(data, 1)
        amount, data = VarInt(data, 2)
        return Token(amount, denom), data


class StringToken(Token):
    """
    The same thing as a Token, like literally, the same thing
    Except that the JSON for the amount is a StringVarInt
    See StringVarInt
    """
    def __init__(self, amount, denom):
        dict.__init__(self, amount=StringVarInt(amount), denom=denom)


class Input(Amino):
    def __init__(self, address, coins):
        dict.__init__(self, address=address, coins=coins)

    def encode(self, field_id=None):
        buf = Address(self['address']).encode(1)
        buf += Repeated(self['coins']).encode(2)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    @staticmethod
    def decode(data, field_id=None, hrp='bnb'):
        if field_id is not None:
            prefix = make_prefix(field_id, 2)
            for i in range(len(prefix)):
                if prefix[i] != data[i]:
                    return None, data
            data = data[len(field_id):]
        address, data = Address.decode(data, 1, hrp)
        coins, data = Repeated.decode(data, 2, Token)
        return Input(address, coins), data


Output = Input
