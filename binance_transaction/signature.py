from binance_transaction.base import Amino, Bytes, StringVarInt, VarInt, make_prefix


"""
signature.py

Cryptographic transaction components

* PubKeySecp256k1
* BnbSignature
"""


class PubKeySecp256k1(Amino):
    def __init__(self, pub_key):
        dict.__init__(self, pub_key=Bytes(pub_key))

    @staticmethod
    def object_id():
        # tendermint/PubKeySecp256k1
        return bytes.fromhex('EB5AE987')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += self['pub_key'].encode()
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    def decode(data, field_id=None):
        if field_id is not None:
            prefix = make_prefix(field_id, 2)
            for i in range(len(prefix)):
                if prefix[i] != data[i]:
                    return VarInt(0), data
            data = data[len(prefix):]
        assert data[0:4] == PubKeySecp256k1.object_id()
        data = data[4:]
        pub_key, data = Bytes.decode(data)
        return PubKeySecp256k1(pub_key), data


class BnbSignature(Amino):
    def __init__(self, pub_key, signature, account_number, sequence):
        dict.__init__(
            self,
            pub_key=PubKeySecp256k1(pub_key),
            signature=Bytes(signature),
            account_number=StringVarInt(account_number),
            sequence=StringVarInt(sequence)
        )

    def encode(self, field_id):
        buf = self['pub_key'].encode(1)
        buf += self['signature'].encode(2)
        buf += self['account_number'].encode(3)
        buf += self['sequence'].encode(4)
        return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    @staticmethod
    def decode(data, field_id):
        if field_id is not None:
            prefix = make_prefix(field_id, 2)
            for i in range(len(prefix)):
                if prefix[i] != data[i]:
                    return VarInt(0), data
            data = data[len(prefix):]
        pub_key, data = PubKeySecp256k1.decode(data, 1)
        signature, data = Bytes.decode(data, 2)
        account_number, data = VarInt.decode(data, 3)
        sequence, data = VarInt.decode(data, 4)
        return BnbSignature(pub_key, signature, account_number, sequence), data
