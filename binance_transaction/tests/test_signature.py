import base64

from binance_transaction.signature import PubKeySecp256k1
from binance_transaction.base import Bytes


def test_pubkey_encoding():
    public_key = bytes.fromhex('020BD40F225A57ED383B440CF073BC5539D0341F5767D2BF2D78406D00475A2EE9')
    public_key_b64 = base64.b64encode(public_key).decode('utf8')
    amino_pubkey = PubKeySecp256k1(Bytes(public_key_b64))
    encoded = amino_pubkey.encode()
    assert encoded == bytes.fromhex('EB5AE98721020BD40F225A57ED383B440CF073BC5539D0341F5767D2BF2D78406D00475A2EE9')
    decoded, remaining = PubKeySecp256k1.decode(encoded)
    assert decoded == amino_pubkey
    assert remaining == b''
