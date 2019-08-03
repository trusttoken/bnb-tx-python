from binance_transaction.base import Repeated, Amino, String, StringVarInt, VarInt
from binance_transaction.crypto import compress_key, int_to_bytes, int_from_bytes, secp256k1
from binance_transaction.signature import BnbSignature
from binance_transaction.msg import Msg


import base64
import hashlib
import json


"""
bnb_transaction.py

Higher-level transaction objects

* BnbTransaction
* TestBnbTransaction
"""


class BnbTransaction(Amino):
    """
    Mainnet transaction
    """
    @staticmethod
    def chain_id():
        return String("Binance-Chain-Tigris")

    def __init__(self, account_number, sequence, source='887'):
        dict.__init__(
            self,
            account_number=StringVarInt(account_number),
            sequence=StringVarInt(sequence),
            source=StringVarInt(source),
            msgs=Repeated([]),
            chain_id=self.chain_id(),
            memo='',
            signatures=Repeated([]),
            data=None
        )

    def signing_json(self):
        return json.dumps({
            "account_number": self['account_number'],
            "chain_id": self['chain_id'],
            "data": self['data'],
            "memo": self['memo'],
            "msgs": self['msgs'],
            "sequence": self['sequence'],
            "source": self['source'],
        }, sort_keys=True, separators=(',', ':')).encode('utf8')

    def signing_hash(self):
        signing_bytes = self.signing_json()
        signing_hash = hashlib.sha256(signing_bytes).digest()
        return signing_hash

    def hash(self):
        return hashlib.sha256(self.encode()).digest()

    def apply_sig(self, signature, public_key):
        assert len(signature) == 64
        if len(public_key) == 65:
            # compress uncompressed public key
            public_key = compress_key(public_key)
        assert len(public_key) == 33
        if int_from_bytes(signature[32:64]) > secp256k1['base'] // 2:
            # Enforce low S (EIP2)
            r = signature[0:32]
            s = int_to_bytes(secp256k1['base'] - int_from_bytes(signature[32:64]), 32)
            signature = r + s
        self['signatures'].append(BnbSignature(
            base64.b64encode(public_key).decode('utf8'),
            base64.b64encode(signature).decode('utf8'),
            self['account_number'],
            self['sequence']
        ))

    def remove_sig(self):
        self['signatures'] = Repeated([])

    def add_msg(self, msg):
        self['msgs'].append(msg)

    @staticmethod
    def object_id():
        return bytes.fromhex('F0625DEE')

    def encode(self):
        buf = self.object_id()
        buf += self['msgs'].encode(1)
        buf += self['signatures'].encode(2)
        buf += self['memo'].encode(3)
        buf += self['source'].encode(4)
        if self['data'] is not None:
            buf += self['data'].encode(5)
        return VarInt(len(buf)).encode() + buf

    @classmethod
    def decode(klass, data):
        assert data[0:4] == klass.object_id()
        data = data[4:]
        msgs, data = Repeated.decode(data, 1, Msg)
        signatures, data = Repeated.decode(data, 2, BnbSignature)
        memo, data = String.decode(data, 3)
        source, data = StringVarInt.decode(data, 4)
        tx_data, data = String.decode(data, 5)
        account_number = signatures[0]['account_number']
        sequence = signatures[0]['sequence']
        tx = klass(msgs, account_number, sequence, source)
        tx['msgs'] = msgs
        tx['signatures'] = signatures
        tx['chain_id'] = klass.chain_id()
        return tx, data

    @classmethod
    def from_obj(klass, transaction_data):
        tx = klass(
            StringVarInt(transaction_data['account_number']),
            StringVarInt(transaction_data['sequence']),
            StringVarInt(transaction_data.get('source', 0))
        )
        tx['memo'] = String(transaction_data['memo'])
        for msg in transaction_data['msgs']:
            tx.add_msg(Msg.from_msg_obj(msg))
        return tx


class TestBnbTransaction(BnbTransaction):
    """
    Testnet transaction
    """
    @staticmethod
    def chain_id():
        return String("Binance-Chain-Nile")
