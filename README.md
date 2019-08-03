# Binance Chain Transaction Library
This library provides a low-level interface for interacting with different Binance Chain transactions.

## Installation
```sh
pip3 install bnb-tx
```

Or, in your `Pipfile`:
```
bnb-tx = "==0.0.4"
```


## Usage
The following is an example that uses the `ecdsa` library to sign.

```python3
import ecdsa
def uncompressed_public_key(sk):
    """ Derive uncompressed public key """
    order = sk.curve.generator.order()
    p = sk.verifying_key.pubkey.point
    x_str = ecdsa.util.number_to_string(p.x(), order)
    y_str = ecdsa.util.number_to_string(p.y(), order)
    uncompressed = b'\x04' + x_str + y_str
    return uncompressed


from binance_transaction import BnbTransaction, NewOrder, address_bytes, BUY, GTE, LIMIT_ORDER

sk = ecdsa.SigningKey.from_pem(open('secp256k1-key.pem').read())
from_address = 'bnb100dxzy02a6k7vysc5g4kk4fqamr7jhjg4m83l0'
account_number = 96025  # https://docs.binance.org/api-reference/dex-api/paths.html#apiv1accountaddress
sequence_number = 888
tx = BnbTransaction(account_number, sequence_number)
order_id = f'{address_bytes(from_address).hex().upper()}-{sequence_number + 1}'
tx.add_msg(NewOrder(from_address, order_id, 'BNB_TUSDB-888', LIMIT_ORDER, BUY, 3500000000, 500000000, GTE))
print(tx.signing_json())
sig = sk.sign_digest(tx.signing_hash())
public_key = uncompressed_public_key(sk)
tx.apply_sig(sig, public_key)
signed_transaction_bytes = tx.encode()
print(f'Signed bytes: {signed_transaction_bytes.hex()}')
```

## Support
Not all transaction types are supported.
Please consult this table for details.
If you need support, please submit a [pull request](https://github.com/trusttoken/bnb-tx-python/pulls).

|  Message Type | encode | decode | from\_obj |
|---------------|--------|--------|-----------|
| Send          | ✅     |        | ✅        |
| NewOrder      | ✅     |        | ✅        |
| CancelOrder   | ✅     |        | ✅        |
| Issue         | ✅     |        | ✅        |
| Mint          | ✅     |        | ✅        |
| Burn          | ✅     |        | ✅        |
| Freeze        | ✅     |        | ✅        |
| Unfreeze      | ✅     |        | ✅        |
| TimeLock      | ✅     |        | ✅        |
| TimeUnlock    | ✅     |        | ✅        |
| TimeRelock    | ✅     |        | ✅        |
| Proposal      | ✅     |        | ✅        |
| Vote          | ✅     |        | ✅        |



## Contributing
See [CONTRIBUTING](CONTRIBUTING.md).


## License
LGPLv3
