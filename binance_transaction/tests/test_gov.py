import base64
import hashlib

from .bnb_transaction import BnbTransaction
from .crypto import verify_sig, uncompress_key


def test_vote_encoding():
    valid_tx_hash = bytes.fromhex('8B57150E0A57F88BA3F7821EF9468C9A64F0E9D7CB470CE158A48A9520E4358D')
    valid_tx = bytes.fromhex(
        '9601F0625DEE0A1EA1CADD36083A1214E536C4580B28F72AA78BD3C730812C7F4FAA05D31801126E0A26EB5AE987210252BF' +
        'F8BFEF6B650D87E6BEBC90E0EE3C08AACB208F483FC646D320AD19149E711240391E522EFB3AE41F6B25884C801F067B2FA1' +
        '051DBE5BF9727F55C2EFC89B7F7C3D5B77CB96A862442575125E3210E64F8518CBFE615EE0C617059294611567631813202E' +
        '2003'
    )
    from_address = 'bnb1u5mvgkqt9rmj4fut60rnpqfv0a865pwnn90v9q'
    assert valid_tx_hash == hashlib.sha256(valid_tx).digest()
    tx = BnbTransaction.from_obj({
        'account_number': 19,
        'from': from_address,
        'memo': '',
        'msgs': [
            {
                'type': 'cosmos-sdk/MsgVote',
                'option': 'Yes',
                'voter': from_address,
                'proposal_id': '58',
            }
        ],
        'source': '3',
        'sequence': '46'
    })
    valid_sig = base64.b64decode(
        'OR5SLvs65B9rJYhMgB8Gey+hBR2+W/lyf1XC78ibf3w9W3fLlqhiRCV1El4yEOZPhRjL/mFe4MYXBZKUYRVnYw=='
    )
    valid_public_key = base64.b64decode('AlK/+L/va2UNh+a+vJDg7jwIqssgj0g/xkbTIK0ZFJ5x')
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'


def test_proposal_encoding():
    valid_tx_hash = bytes.fromhex('2957AB7430288A3C787A247FBADED70649210FA2F9EDD67874314B349DB6530E')
    valid_sig = base64.b64decode(
        'UaIOIJW6PkOjmF+kMojJxpMmGVJc6PnnRjyFpgFGeBAiETanwvWp1vUFNHT5hyh42+nP2dpJCTeSIJBj5NkVYw==')
    valid_public_key = base64.b64decode('Aut6gsEmgMh2JxOqvEe6zswkEbSbcVDPIeKqndFiF3IB')
    valid_tx = bytes.fromhex(
        'DB02F0625DEE0AE301B42D614E0A116C697374204D4954482D4337362F424E42129B017B22626173655F61737365745F7379' +
        '6D626F6C223A224D4954482D433736222C2271756F74655F61737365745F73796D626F6C223A22424E42222C22696E69745F' +
        '7072696365223A3233303030302C226465736372697074696F6E223A226C697374204D4954482D4337362F424E42222C2265' +
        '78706972655F74696D65223A22323031392D30342D32375431383A30303A30302B30383A3030227D18042214A5870BE8CA8D' +
        '62085927D61CFBF458BFE81B25D42A0C0A03424E421080D0DBC3F4023080E098D4DAEE02126F0A26EB5AE9872102EB7A82C1' +
        '2680C8762713AABC47BACECC2411B49B7150CF21E2AA9DD162177201124051A20E2095BA3E43A3985FA43288C9C693261952' +
        '5CE8F9E7463C85A601467810221136A7C2F5A9D6F5053474F9872878DBE9CFD9DA49093792209063E4D9156318B7052001'
    )
    assert valid_tx_hash == hashlib.sha256(valid_tx).digest()
    description = (
        "{\"base_asset_symbol\":\"MITH-C76\",\"quote_asset_symbol\":\"BNB\",\"init_price\":230000," +
        "\"description\":\"list MITH-C76/BNB\",\"expire_time\":\"2019-04-27T18:00:00+08:00\"}"
    )
    from_address = 'bnb15krsh6x2343qskf86cw0hazchl5pkfw53zllut'
    tx = BnbTransaction.from_obj({
        'account_number': 695,
        'sequence': 1,
        'from': from_address,
        'source': '0',
        'memo': '',
        'msgs': [
            {
                'type': 'cosmos-sdk/MsgSubmitProposal',
                'title': 'list MITH-C76/BNB',
                'description': description,
                'proposal_type': 'ListTradingPair',
                'proposer': from_address,
                'initial_deposit': [{
                    'amount': '100000000000',
                    'denom': 'BNB',
                }],
                'voting_period': '12600000000000'
            }
        ]
    })
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    assert valid_tx_hash == tx.hash()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'


def test_recent_proposal():
    valid_tx_hash = bytes.fromhex('A531406A5C4926EDF60A600FDECED280439E8BBEAD99460C60BE8F913588A196')
    from_address = 'bnb1xljnjk7msm5t5lwp4zv2ua80rrxzn2s2afce4j'
    valid_pubkey = base64.b64decode('A27f07q13gBGytyhIuID9XnnPHS8NnJIpZKO1gGtIwPm')
    valid_sig = base64.b64decode(
        'l8aL4qYXAZSdtb8z7rtw3PIx2T21XPL1ZW8mGLmLUY5sYvsoELWrIMPiEcpfgWb5/QRaaXIML9gI3FzTJgd0Bg==')
    description = (
        "{\"base_asset_symbol\":\"NODE-F3A\",\"quote_asset_symbol\":\"BNB\",\"init_price\":2941176," +
        "\"description\":\"list NODE-F3A/BNB\",\"expire_time\":\"2019-10-10T00:00:00Z\"}"
    )
    valid_tx = bytes.fromhex(
        'D802F0625DEE0ADF01B42D614E0A116C697374204E4F44452D4633412F424E421297017B22626173655F61737365745F7379' +
        '6D626F6C223A224E4F44452D463341222C2271756F74655F61737365745F73796D626F6C223A22424E42222C22696E69745F' +
        '7072696365223A323934313137362C226465736372697074696F6E223A226C697374204E4F44452D4633412F424E42222C22' +
        '6578706972655F74696D65223A22323031392D31302D31305430303A30303A30305A227D1804221437E5395BDB86E8BA7DC1' +
        'A898AE74EF18CC29AA0A2A0B0A03424E42108094EBDC033080809CDE91E7B00112700A26EB5AE98721036EDFD3BAB5DE0046' +
        'CADCA122E203F579E73C74BC367248A5928ED601AD2303E6124097C68BE2A61701949DB5BF33EEBB70DCF231D93DB55CF2F5' +
        '656F2618B98B518E6C62FB2810B5AB20C3E211CA5F8166F9FD045A69720C2FD808DC5CD326077406189DDB012003'
    )
    assert hashlib.sha256(valid_tx).digest() == valid_tx_hash
    tx = BnbTransaction.from_obj({
        'account_number': 28061,
        'sequence': 3,
        'from': from_address,
        'source': '0',
        'memo': '',
        'msgs': [
            {
                'type': 'cosmos-sdk/MsgSubmitProposal',
                'title': "list NODE-F3A/BNB",
                'description': description,
                'proposal_type': 'ListTradingPair',
                'proposer': from_address,
                'initial_deposit': [{
                    'amount': '1000000000',
                    'denom': 'BNB',
                }],
                'voting_period': '777600000000000'
            }
        ]
    })
    tx.apply_sig(valid_sig, uncompress_key(valid_pubkey))
    assert valid_tx == tx.encode()
    tx.remove_sig()
    print(tx.signing_json())
    valid_signing_bytes = bytes.fromhex(
        '7B226163636F756E745F6E756D626572223A223238303631222C22636861696E5F6964223A2242696E616E63652D43686169' +
        '6E2D546967726973222C2264617461223A6E756C6C2C226D656D6F223A22222C226D736773223A5B7B226465736372697074' +
        '696F6E223A227B5C22626173655F61737365745F73796D626F6C5C223A5C224E4F44452D4633415C222C5C2271756F74655F' +
        '61737365745F73796D626F6C5C223A5C22424E425C222C5C22696E69745F70726963655C223A323934313137362C5C226465' +
        '736372697074696F6E5C223A5C226C697374204E4F44452D4633412F424E425C222C5C226578706972655F74696D655C223A' +
        '5C22323031392D31302D31305430303A30303A30305A5C227D222C22696E697469616C5F6465706F736974223A5B7B22616D' +
        '6F756E74223A2231303030303030303030222C2264656E6F6D223A22424E42227D5D2C2270726F706F73616C5F7479706522' +
        '3A224C69737454726164696E6750616972222C2270726F706F736572223A22626E6231786C6A6E6A6B376D736D3574356C77' +
        '70347A7632756138307272787A6E32733261666365346A222C227469746C65223A226C697374204E4F44452D4633412F424E' +
        '42222C22766F74696E675F706572696F64223A22373737363030303030303030303030227D5D2C2273657175656E6365223A' +
        '2233222C22736F75726365223A2230227D'
    )
    print(valid_signing_bytes)
    assert tx.signing_json() == valid_signing_bytes
    assert verify_sig(uncompress_key(valid_pubkey), tx.signing_hash(), valid_sig), 'Wrong json encoding'
