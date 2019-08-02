import base64
import hashlib


from .bnb_transaction import BnbTransaction
from .crypto import uncompress_key, verify_sig


def test_new_order():
    valid_tx_hash = bytes.fromhex('7EDD4657C441C68D7D345875A80E3A10B942BDA96188C937997E843CCE284209')
    valid_tx = bytes.fromhex(
        'E001F0625DEE0A66CE6DC0430A140917565C2C7CC07696435D13B40B438BE38FADC6122A3039313735363543324337434330'
        '37363936343335443133423430423433384245333846414443362D381A0D524156454E2D4636365F424E422002280230BC50'
        '3880C0DFDA8EE906400312700A26EB5AE9872102D08F5389E408E26134C7EBA87119A2814DE924EEE5C61E1ED99D6F468256'
        '64AC1240CF4D2BE853D8EBA348353A91ED3BCF2C0164004DAF898153444E91E4A2BAC02106E4D1B3686D70F2B756274D90BF'
        '120BA87A3CCC412E1D20618CAB480CE69A5718C7A00420072002'
    )
    assert hashlib.sha256(valid_tx) == valid_tx_hash
    from_address = 'bnb1pyt4vhpv0nq8d9jrt5fmgz6r303cltwxu27xn2'
    tx = BnbTransaction.from_obj({
        'account_number': 69703,
        'from': from_address,
        'memo': '',
        'msgs': [
            {
                'type': 'dex/NewOrder',
                'id': '0917565C2C7CC07696435D13B40B438BE38FADC6-8',
                'ordertype': 2,
                'price': 10300,
                'quantity': 30000000000000,
                'sender': from_address,
                'side': 2,
                'symbol': 'RAVEN-F66_BNB',
                'timeinforce': 3
            }
        ],
        'sequence': 7,
        'source': 2
    })
    valid_public_key = base64.b64decode(
        'AtCPU4nkCOJhNMfrqHEZooFN6STu5cYeHtmdb0aCVmSs',
    )
    valid_sig = base64.b64decode(
        'z00r6FPY66NINTqR7TvPLAFkAE2viYFTRE6R5KK6wCEG5NGzaG1w8rdWJ02QvxILqHo8zEEuHSBhjKtIDOaaVw=='
    )
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    print(valid_tx.hex())
    print(tx.encode().hex())
    assert valid_tx == tx.encode()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'


def test_cancel_order():
    valid_tx_hash = bytes.fromhex('E28E8BEA823FCBD64FC9825932ED98CFDCE36447EF651AD1D0534B6C167A1911')
    valid_tx = bytes.fromhex(
        'CD01F0625DEE0A53166E681B0A14915734BD8050E5AA03F9D056ECC1F695E86CC9BF120B544F502D3439315F424E421A2A39'
        '3135373334424438303530453541413033463944303536454343314636393545383643433942462D3212700A26EB5AE98721'
        '030D56B78B7BA4DDE1D50D05C2D06ED334716A88C7A6E10ACC68F82A711882D1F31240B0E10084BCF273B6873A7F275EB195'
        '788A7054E48DCA0CB5AEC745467F19AAA46120236C3220D65E2C2801184773DC4E32EE8F33CE87DC13951E5818723CC60318'
        '98910920022001'
    )
    assert hashlib.sha256(valid_tx) == valid_tx_hash
    from_address = 'bnb1j9tnf0vq2rj65qle6ptwes0kjh5xejdle3fpuj'
    tx = BnbTransaction.from_obj({
        'account_number': 149656,
        'from': from_address,
        'memo': '',
        'msgs': [
            {
                'type': 'dex/CancelOrder',
                'refid': '915734BD8050E5AA03F9D056ECC1F695E86CC9BF-2',
                'sender': from_address,
                'symbol': 'TOP-491_BNB'
            }
        ],
        'sequence': 2,
        'source': 1
    })
    valid_public_key = base64.b64decode(
        'Aw1Wt4t7pN3h1Q0FwtBu0zRxaojHpuEKzGj4KnEYgtHz'
    )
    valid_sig = base64.b64decode(
        'sOEAhLzyc7aHOn8nXrGVeIpwVOSNygy1rsdFRn8ZqqRhICNsMiDWXiwoARhHc9xOMu6PM86H3BOVHlgYcjzGAw=='
    )
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    print(valid_tx.hex())
    print(tx.encode().hex())
    assert valid_tx == tx.encode()
    tx.remove_sig()
    print(tx.signing_json())


def test_listdex():
    valid_tx_hash = bytes.fromhex('2426AF82B24B9F8E126CE386594028BBDEF84F54D73D07CF0F16C40B18D42BF6')
    valid_tx = bytes.fromhex(
        'B201F0625DEE0A38B41DE13F0A14EDB243FACB78CE48A777E2BE7C904D931650AFF4103F1A08425443422D31444522095553' +
        '4453422D314143288090AEEA962112700A26EB5AE9872103FB3D12E8C28238BBD8E96DA24AB8965F4F5AF2A054DED841356E' +
        '39E88F646D6112402487C1CC7515932128F28657BD596AF5256EFADB807B1C2CCEBD1397D75837ED1F1D561F858DE9891291' +
        'F77ABCC36A2B974A5764C58716B565D791651CDFF33B18AA800320032001'
    )
    assert valid_tx_hash == hashlib.sha256(valid_tx).digest()
    tx = BnbTransaction.from_obj({
        'account_number': 49194,
        'from': 'bnb1akey87kt0r8y3fmhu2l8eyzdjvt9ptl5cppz0v',
        'memo': '',
        'msgs': [
            {
                'type': 'dex/ListMsg',
                'init_price': '1140000000000',
                'from': 'bnb1akey87kt0r8y3fmhu2l8eyzdjvt9ptl5cppz0v',
                'proposal_id': '63',
                'quote_asset_symbol': 'USDSB-1AC',
                'base_asset_symbol': 'BTCB-1DE',
            }
        ],
        'source': '1',
        'sequence': '3'
    })
    valid_sig = base64.b64decode(
        'JIfBzHUVkyEo8oZXvVlq9SVu+tuAexwszr0Tl9dYN+0fHVYfhY3piRKR93q8w2orl0pXZMWHFrVl15FlHN/zOw=='
    )
    valid_public_key = base64.b64decode('A/s9EujCgji72Oltokq4ll9PWvKgVN7YQTVuOeiPZG1h')
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'
