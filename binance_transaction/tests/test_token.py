import base64
import hashlib

from .bnb_transaction import BnbTransaction, TestBnbTransaction
from .crypto import uncompress_key, verify_sig


def test_send_signed_encoding():
    valid_tx = bytes.fromhex(
        'D701F0625DEE0A502A2C87FA0A240A14BC44784B0C99AA301DAC66C8A477354E039FDB13120C0A03424E4210EE8389EB900112' +
        '240A148EA70D7D2EA8A14BA2B33D18D5DFBD6FAE0A6EA8120C0A03424E4210EE8389EB900112720A26EB5AE987210217067B36' +
        'F33C1178D09DFB7B8B59853EDC871A7044F2F7DDAD885DDFB353152D1240408B7BC4FE6DB3DEB5632DEB61B3B30A37E7CA8467' +
        '1392DC998F9BF25AA0BD227A3B0BF07237235901A7EBC6D815BEDAD8CCD7D93AF75D8F703D057B24ED0BF818D7F10120A2B601' +
        '1A093130353433343133322001'
    )
    valid_tx_hash = bytes.fromhex('4FE530CE21059C75F03FE89E95756EE7B5EF93002800BA0D93134C440F5BD902')
    assert hashlib.sha256(valid_tx).digest() == valid_tx_hash
    tx = BnbTransaction.from_obj({
        'account_number': 30935,
        'sequence': 23330,
        'from': 'bnb1h3z8sjcvnx4rq8dvvmy2gae4fcpelkcn292qwu',
        'memo': '105434132',
        'msgs': [
            {
                'type': 'cosmos-sdk/Send',
                'inputs': [
                    {
                        'address': 'bnb1h3z8sjcvnx4rq8dvvmy2gae4fcpelkcn292qwu',
                        'coins': [
                            {
                                'amount': '38879248878',
                                'denom': 'BNB'
                            }
                        ]
                    }
                ],
                'outputs': [
                    {
                        'address': 'bnb136ns6lfw4zs5hg4n85vdthaad7hq5m4gtkgf23',
                        'coins': [
                            {
                                'amount': '38879248878',
                                'denom': 'BNB'
                            }
                        ]
                    }
                ]
            }
        ],
        'source': '1'
    })
    valid_sig = bytes.fromhex(
        '408b7bc4fe6db3deb5632deb61b3b30a37e7ca84671392dc998f9bf25aa0bd227a3b0bf07237235901a7ebc6d815bedad8ccd7' +
        'd93af75d8f703d057b24ed0bf8'
    )
    valid_public_key = bytes.fromhex('0217067b36f33c1178d09dfb7b8b59853edc871a7044f2f7ddad885ddfb353152d')
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'


def test_issue_signed_encoding():
    valid_tx = bytes.fromhex(
        'A801F0625DEE0A3317EFAB800A14A5870BE8CA8D62085927D61CFBF458BFE81B25D412074D69746872696C1A044D4954482080' +
        '80A8EC85AFD1B101126D0A26EB5AE9872102EB7A82C12680C8762713AABC47BACECC2411B49B7150CF21E2AA9DD16217720112' +
        '4062437A3A64AEFB6C9C0C29468E0A9CA3DDEC9E8F3F70DFBC67D58A1D7A68BFF841BE5DBEFBE6D3D63622EACE4B30BB61608D' +
        '89059996E8E356740BE54776EDDB18B705'
    )
    valid_tx_hash = bytes.fromhex('C7696AD989D8258FFD85EBE01245EE50EB15756929F03247DFF8B581867B6EC7')
    assert hashlib.sha256(valid_tx).digest() == valid_tx_hash
    from_address = 'bnb15krsh6x2343qskf86cw0hazchl5pkfw53zllut'
    tx = BnbTransaction.from_obj({
        'account_number': 695,
        'sequence': 0,
        'from': from_address,
        'memo': '',
        'msgs': [
            {
                'type': 'tokens/IssueMsg',
                'from': from_address,
                'name': 'Mithril',
                'symbol': 'MITH',
                'total_supply': 100000000000000000,
                'mintable': False
            }
        ],
        'source': '0'
    })
    valid_sig = bytes.fromhex(
        '62437a3a64aefb6c9c0c29468e0a9ca3ddec9e8f3f70dfbc67d58a1d7a68bff841be5dbefbe6d3d63622eace4b30bb61608d89' +
        '059996e8e356740be54776eddb'
    )
    valid_public_key = bytes.fromhex('02eb7a82c12680c8762713aabc47bacecc2411b49b7150cf21e2aa9dd162177201')
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    assert valid_tx_hash == tx.hash()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'


def test_self_issue():
    from_address = 'tbnb100zjwtsfhaenvadlf50yaakkq7aksmvrlyxrek'
    account_number = 675053
    """
    valid_tx = bytes.fromhex(
        'ac01f0625dee0a3617efab800a147bc5272e09bf733675bf4d1e4ef6d607bb686d831207547275655553441a055455534442' +
        '20ffff8f948e8a9bf37c2801126e0a26eb5ae987210259107ce022c1ab227b6342e16906d43fe91adcec957edbe549ab9338' +
        '1634d1181240ac4889c873185c5fb8a66077b5917b1ca0554c5d09ba654d75193f68a5f302591744d2c4374c4057ded69d9c' +
        '03716522305483162c2302b7ecfd16be7ab76c6318ed9929'
    )
    """
    tx = TestBnbTransaction.from_obj({
        'account_number': account_number,
        'from': from_address,
        'sequence': 0,
        'memo': '',
        'msgs': [
            {
                'type': 'tokens/IssueMsg',
                'from': from_address,
                'name': 'TrueUSD',
                'symbol': 'TUSDB',
                'total_supply': 8999999999999999999,
                'mintable': True
            }
        ],
        'source': '0'
    })
    valid_public_key = bytes.fromhex(
        '0459107ce022c1ab227b6342e16906d43fe91adcec957edbe549ab93381634d118bf3359a4f5c441f31e2e036d0848a7a651' +
        'feaba78aefb045d88ad1db6cccb42a')
    valid_sig = bytes.fromhex(
        'ac4889c873185c5fb8a66077b5917b1ca0554c5d09ba654d75193f68a5f302591744d2c4374c4057ded69d9c037165223054' +
        '83162c2302b7ecfd16be7ab76c63')
    print(valid_sig.hex())
    print(tx.signing_hash().hex())
    print(valid_public_key.hex())
    assert verify_sig(valid_public_key, tx.signing_hash(), valid_sig)


def test_testnet_issue_asset_encoding():
    valid_tx_hash = bytes.fromhex('3B60DA53BFC95518B63ABB3278FF458E70855CF2F7338006C6004C974283E53D')
    valid_tx = bytes.fromhex(
        'B301F0625DEE0A3D17EFAB800A142EFCF63F8A085B3B7C2CD3FDF8E11BA2413548B31212547269706C65204120424E422054' +
        '6F6B656E1A06414141424E422080ADE2042801126E0A26EB5AE98721034DBF7CA73DEEF49FC16D906382140F3BAEA840247E' +
        '52365B47782D351FB154301240993D4B4CCFC515C191A94D01793FB4018A09872B0B29C9A9FAE7B7959EA2CE316F0209E86D' +
        'A29407910790D524B585C3CC0401BE4523863273C1241BF143F3F518A4F401'
    )
    assert valid_tx_hash == hashlib.sha256(valid_tx).digest()
    valid_sig = base64.b64decode(
        'mT1LTM/FFcGRqU0BeT+0AYoJhysLKcmp+ue3lZ6izjFvAgnobaKUB5EHkNUktYXDzAQBvkUjhjJzwSQb8UPz9Q=='
    )
    valid_public_key = base64.b64decode('A02/fKc97vSfwW2QY4IUDzuuqEAkflI2W0d4LTUfsVQw')
    tx = TestBnbTransaction.from_obj({
        'account_number': 31268,
        'from': 'tbnb19m70v0u2ppdnklpv607l3cgm5fqn2j9n3r4j09',
        'sequence': 0,
        'memo': '',
        'msgs': [
            {
                'type': 'tokens/IssueMsg',
                'from': 'tbnb19m70v0u2ppdnklpv607l3cgm5fqn2j9n3r4j09',
                'name': 'Triple A BNB Token',
                'symbol': 'AAABNB',
                'total_supply': 10000000,
                'mintable': True
            }
        ],
        'source': '0'
    })
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    print(valid_tx)
    print(tx.encode())
    assert valid_tx == tx.encode()
    tx.remove_sig()
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig)


def test_recent_issue_asset_encoding():
    valid_tx_hash = bytes.fromhex('1AC6A272F3FECF1B2B98DE720E916C97B5BD9857722879D239CC93F192CA5DA8')
    valid_tx = bytes.fromhex(
        'AB01F0625DEE0A3317EFAB800A149A68092EE3D99C69A70BAC9EEAE16F8A5175DC0A1204555344531A055553445342208080' +
        '90948E8A9BF37C280112700A26EB5AE98721024A754FAF37E8C48BEE248A8094BC24E8FA601CD5EE83F7DD96C00574CE09DC' +
        'AE1240128FAC6859D4101409287C5968D55AE5A23C74D1863B8384D4CA0475857CD95E1A14A86AFCC5E2AA777D854A92A466' +
        '66123B49C403DA3C2CB25E3617E94F854118D5C5012007'
    )
    assert valid_tx_hash == hashlib.sha256(valid_tx).digest()
    valid_sig = base64.b64decode(
        'Eo+saFnUEBQJKHxZaNVa5aI8dNGGO4OE1MoEdYV82V4aFKhq/MXiqnd9hUqSpGZmEjtJxAPaPCyyXjYX6U+FQQ=='
    )
    valid_public_key = base64.b64decode('Akp1T6836MSL7iSKgJS8JOj6YBzV7oP33ZbABXTOCdyu')
    tx = BnbTransaction.from_obj({
        'account_number': 25301,
        'from': 'bnb1nf5qjthrmxwxnfct4j0w4ct03fghthq24qt990',
        'sequence': 7,
        'memo': '',
        'msgs': [
            {
                'type': 'tokens/IssueMsg',
                'from': 'bnb1nf5qjthrmxwxnfct4j0w4ct03fghthq24qt990',
                'name': 'USDS',
                'symbol': 'USDSB',
                'total_supply': 9000000000000000000,
                'mintable': True
            }
        ]
    })
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    tx.remove_sig()
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig)


def test_recent_testnet_issue_encoding():
    valid_tx_hash = bytes.fromhex('FC3F515D12F1E7D081E3104462058BE23C9B7A89E8D2BE10231E001008E295B9')
    valid_tx = bytes.fromhex(
        'AD01F0625DEE0A3517EFAB800A14E5277642209E466D8028DAA535363CA65843E05C120A5A65626920436F696E311A035A43' +
        '31208080A8EC85AFD1B10112700A26EB5AE98721038C6549473BA7D9993EE4059AC9DF52B152F492DAB81EF42ED008A34306' +
        'C99DF9124035A8F4F1F93E77474A398C00E1387AF22C9A8E271E53DAAA1EF68B87F9E948E0349E82929CBB157BD057E181FF' +
        '717B4D5F89A0EC1DF29AAD365A390C20E7C8D318FDB2292001'
    )
    assert valid_tx_hash == hashlib.sha256(valid_tx).digest()
    valid_sig = base64.b64decode(
        'Naj08fk+d0dKOYwA4Th68iyajiceU9qqHvaLh/npSOA0noKSnLsVe9BX4YH/cXtNX4mg7B3ymq02WjkMIOfI0w==')
    valid_public_key = base64.b64decode('A4xlSUc7p9mZPuQFmsnfUrFS9JLauB70LtAIo0MGyZ35')
    from_address = 'tbnb1u5nhvs3qnerxmqpgm2jn2d3u5evy8czuvt0m95'
    tx = TestBnbTransaction.from_obj({
        'account_number': 678269,
        'from': from_address,
        'sequence': 1,
        'memo': '',
        'msgs': [
            {
                'type': 'tokens/IssueMsg',
                'from': from_address,
                'name': 'Zebi Coin1',
                'symbol': 'ZC1',
                'total_supply': 100000000000000000,
                'mintable': False
            }
        ]
    })
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    assert valid_tx_hash == tx.hash()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'


def test_mint_testnet_encoding():
    valid_tx_hash = bytes.fromhex('8A7F869A38A2545A6E522601B19A948E2D66317BB9F8BE9B1711DD8357E9A44F')
    valid_tx = bytes.fromhex(
        'A601F0625DEE0A2E467E08290A142EFCF63F8A085B3B7C2CD3FDF8E11BA2413548B3120A414141424E422D334236188095DE' +
        'AEB1DE1612700A26EB5AE98721034DBF7CA73DEEF49FC16D906382140F3BAEA840247E52365B47782D351FB154301240BFCE' +
        'B70AE5646123443B77EA9E8FD566A8249A22C5E3B3ECB192983FE74B47EF085BAB21056790CDE74E41A61E605D6C3F7B944F' +
        'ADEB29431AFD97251CFE13C918A4F4012001'
    )
    assert hashlib.sha256(valid_tx).digest() == valid_tx_hash
    valid_sig = base64.b64decode(
        'v863CuVkYSNEO3fqno/VZqgkmiLF47PssZKYP+dLR+8IW6shBWeQzedOQaYeYF1sP3uUT63rKUMa/ZclHP4TyQ==')
    valid_public_key = base64.b64decode('A02/fKc97vSfwW2QY4IUDzuuqEAkflI2W0d4LTUfsVQw')
    tx = TestBnbTransaction.from_obj({
        'account_number': 31268,
        'from': 'tbnb19m70v0u2ppdnklpv607l3cgm5fqn2j9n3r4j09',
        'sequence': 1,
        'memo': '',
        'msgs': [
            {
                'type': 'tokens/MintMsg',
                'from': 'tbnb19m70v0u2ppdnklpv607l3cgm5fqn2j9n3r4j09',
                'symbol': 'AAABNB-3B6',
                'amount': 100000090000000,
            }
        ],
        'source': '0'
    })
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    print(valid_tx)
    print(tx.encode())
    assert tx.encode() == valid_tx
    tx.remove_sig()
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'


def test_burn():
    valid_tx_hash = bytes.fromhex('89BFE0037ED2A13E507FBAD452E8267397DB0A54B81DF227B6150CDB6094FCE5')
    valid_tx = bytes.fromhex(
        'A801F0625DEE0A307ED2D2A00A149A68092EE3D99C69A70BAC9EEAE16F8A5175DC0A120A555344532E422D43323718808090' +
        '948E8A9BF37C12700A26EB5AE98721024A754FAF37E8C48BEE248A8094BC24E8FA601CD5EE83F7DD96C00574CE09DCAE1240' +
        '64FDC6E9FDF19DDB5CCFC148187D67A80E41AEF590D5C38AC425F3114D2245EC290FFFDEA422C798360421B3F5E66797C340' +
        'DBF183CA1CC5184956D10D5987E818D5C5012006'
    )
    assert valid_tx_hash == hashlib.sha256(valid_tx).digest()
    from_address = 'bnb1nf5qjthrmxwxnfct4j0w4ct03fghthq24qt990'
    valid_public_key = base64.b64decode('Akp1T6836MSL7iSKgJS8JOj6YBzV7oP33ZbABXTOCdyu')
    valid_sig = base64.b64decode(
        "ZP3G6f3xndtcz8FIGH1nqA5BrvWQ1cOKxCXzEU0iRewpD//epCLHmDYEIbP15meXw0Db8YPKHMUYSVbRDVmH6A==")
    tx = BnbTransaction.from_obj({
        'account_number': 25301,
        'from': from_address,
        'memo': '',
        'msgs': [
            {
                'type': 'tokens/BurnMsg',
                'amount': 9000000000000000000,
                'from': from_address,
                'symbol': "USDS.B-C27",
            }
        ],
        'sequence': '6',
        'source': '0'
    })
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'


def test_freeze():
    valid_tx_hash = bytes.fromhex('B06C319E2CFEF19FD65DB485585BA8DB6C241A8143F39F4436B14949C4BAAC99')
    valid_tx = bytes.fromhex(
        'A401F0625DEE0A2BE774B32D0A141AD3AB3E43C28AC9A9083878E2DECA092B09DAFC12075048422D32444618909AD79FA680' +
        '02126F0A26EB5AE9872103F405490307AC7FBC888F3CB13D6D9162845EF5DFC233158BFEF0DD9E2F3599DA1240DFAC8DF469' +
        '000B73AF1492458BDBBF00FE2D9E7300A61EFAA72C8F084DA36712589A66C0785148CF2839F74022B072519D2431A124610C' +
        'F491A5F00F8B62FE4B18C66C205B2001'
    )
    assert valid_tx_hash == hashlib.sha256(valid_tx).digest()
    valid_sig = base64.b64decode(
        '36yN9GkAC3OvFJJFi9u/AP4tnnMAph76pyyPCE2jZxJYmmbAeFFIzyg590AisHJRnSQxoSRhDPSRpfAPi2L+Sw=='
    )
    valid_public_key = base64.b64decode('A/QFSQMHrH+8iI88sT1tkWKEXvXfwjMVi/7w3Z4vNZna')
    tx = BnbTransaction.from_obj({
        'account_number': 13894,
        'from': 'bnb1rtf6k0jrc29vn2gg8puw9hk2py4snkhuez89fk',
        'memo': '',
        'msgs': [
            {
                'type': 'tokens/FreezeMsg',
                'amount': 8806360010000,
                'from': 'bnb1rtf6k0jrc29vn2gg8puw9hk2py4snkhuez89fk',
                'symbol': 'PHB-2DF'
            }
        ],
        'source': '1',
        'sequence': '91'
    })
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'


def test_unfreeze():
    valid_tx_hash = bytes.fromhex('85A02C52AA88005D807049053D59B86D96469F595820ECE11B283CF78C50E4A0')
    valid_tx = bytes.fromhex(
        'A301F0625DEE0A2A6515FF0D0A141AD3AB3E43C28AC9A9083878E2DECA092B09DAFC12075048422D32444618A0ADBFF5FE20' +
        '126F0A26EB5AE9872103F405490307AC7FBC888F3CB13D6D9162845EF5DFC233158BFEF0DD9E2F3599DA12409E0734BFE788' +
        '309C51C752D8D998530693CFD5A33A2865A92E41C9B1127DF4D45CDE81F47ABA6E258886E3841F7A867C6F93165F2D76D07D' +
        'D97FD0ED8878102018C66C20532001'
    )
    assert valid_tx_hash == hashlib.sha256(valid_tx).digest()
    valid_sig = base64.b64decode(
        'ngc0v+eIMJxRx1LY2ZhTBpPP1aM6KGWpLkHJsRJ99NRc3oH0erpuJYiG44QfeoZ8b5MWXy120H3Zf9DtiHgQIA=='
    )
    valid_public_key = base64.b64decode('A/QFSQMHrH+8iI88sT1tkWKEXvXfwjMVi/7w3Z4vNZna')
    tx = BnbTransaction.from_obj({
        'account_number': 13894,
        'from': 'bnb1rtf6k0jrc29vn2gg8puw9hk2py4snkhuez89fk',
        'memo': '',
        'msgs': [
            {
                'type': 'tokens/UnfreezeMsg',
                'amount': 1133580900000,
                'from': 'bnb1rtf6k0jrc29vn2gg8puw9hk2py4snkhuez89fk',
                'symbol': 'PHB-2DF'
            }
        ],
        'source': '1',
        'sequence': '83'
    })
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'


def test_timelock_encoding():
    valid_tx_hash = bytes.fromhex('7617B5B7C96E9FD560826481C79D3579A76B51BC7459F0EFF812F4567667FD89')
    valid_tx = bytes.fromhex(
        'A501F0625DEE0A2F079215310A140B1A85684331AB8C73A6ECBF8B2A02DF379E0E2F1204746573741A070A03424E42100120'
        'F587BBE905126E0A26EB5AE987210350BE56D54E71C36648F4A59518E83E1B78E7A041581A0764AA72E1E9986E029E12404E'
        '5C8823B4CF57371CEE14E21A9589118E2F82271FD426C907673A69E3BB1B7A36046102F6B6AD6E05FEBADD9030BE6F49819B'
        'C7B2FFF5D792EF9D2DB5DF29FE1844200F'
    )
    assert valid_tx_hash == hashlib.sha256(valid_tx).digest()
    from_address = 'bnb1pvdg26zrxx4ccuaxajlck2szmumeur30k2eru9'
    tx = BnbTransaction.from_obj({
        'account_number': 68,
        'from': from_address,
        'memo': '',
        'msgs': [
            {
                'type': 'tokens/TimeLockMsg',
                'from': from_address,
                'description': 'test',
                "lock_time": "1563345909",
                'amount': [
                    {
                        'amount': 1,
                        'denom': 'BNB',
                    }
                ]
            }
        ],
        'source': 0,
        'sequence': 15,
    })
    valid_sig = base64.b64decode(
        'TlyII7TPVzcc7hTiGpWJEY4vgicf1CbJB2c6aeO7G3o2BGEC9ratbgX+ut2QML5vSYGbx7L/9deS750ttd8p/g=='
    )
    valid_public_key = base64.b64decode(
        'A1C+VtVOccNmSPSllRjoPht456BBWBoHZKpy4emYbgKe'
    )
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'


def test_timeunlock_encoding():
    valid_tx_hash = bytes.fromhex('89789C6D36CB0779184CB616D3EC67C453A84D12439E9A25ACCC767EC6CA5F00')
    valid_tx = bytes.fromhex(
        '9201F0625DEE0A1CC4050C6C0A140B1A85684331AB8C73A6ECBF8B2A02DF379E0E2F1010126E0A26EB5AE987210350BE56D5'
        '4E71C36648F4A59518E83E1B78E7A041581A0764AA72E1E9986E029E1240306B11C7173D73A6A43D0C04F2C18453553CD805'
        'E5C56D6F78E5F02D2E32D36B7657045E30EED250D28FA12C17685C5AAE97AD73BF6F3A75986FAF09723E39C418442010'
    )
    assert valid_tx_hash == hashlib.sha256(valid_tx).digest()
    from_address = 'bnb1pvdg26zrxx4ccuaxajlck2szmumeur30k2eru9'
    tx = BnbTransaction.from_obj({
        'account_number': 68,
        'from': from_address,
        'memo': '',
        'msgs': [
            {
                'type': 'tokens/TimeUnlockMsg',
                'from': from_address,
                'time_lock_id': 16,
            }
        ],
        'source': 0,
        'sequence': 16,
    })
    valid_sig = base64.b64decode(
        'MGsRxxc9c6akPQwE8sGEU1U82AXlxW1veOXwLS4y02t2VwReMO7SUNKPoSwXaFxarpetc79vOnWYb68Jcj45xA=='
    )
    valid_public_key = base64.b64decode(
        'A1C+VtVOccNmSPSllRjoPht456BBWBoHZKpy4emYbgKe'
    )
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'


def test_timerelock_encoding():
    valid_tx_hash = bytes.fromhex('FEB4F9C0C33FEF0DE55681B3B5B78BDDCF9FB122DADFB61A8F17247B9D05D006')
    valid_tx = bytes.fromhex(
        'B101F0625DEE0A38504711DA0A14A7838B942F2133409975D9A57EFD5E7E2CE3894510970722080A03424E4210E807220F0A'
        '08455454332D463832108084AF5F12710A26EB5AE98721021C853155A922983F2C938A492B1A7A607C98F40BE72065055111'
        'E90BA87A554E1240AB35604B557E91362BB4CA908EAF6DA5BCE024A7725C6F304D4DA8660084C95D7446646466024F37F58F'
        '467BC9CC647B1A99794386E74EF72113EDFF46DEA3311890E828209907'
    )
    assert valid_tx_hash == hashlib.sha256(valid_tx).digest()
    from_address = 'tbnb157pch9p0yye5pxt4mxjhal270ckw8z29euhxfe'
    tx = TestBnbTransaction.from_obj({
        'account_number': 668688,
        'from': from_address,
        'memo': '',
        'msgs': [
            {
                'type': 'tokens/TimeRelockMsg',
                'from': from_address,
                'lock_time': 0,
                'time_lock_id': 919,
                'description': '',
                'amount': [
                    {
                        'amount': 1000,
                        'denom': 'BNB',
                    },
                    {
                        'amount': 200000000,
                        'denom': 'ETT3-F82',
                    }
                ]
            }
        ],
        'sequence': 921,
        'source': 0
    })
    valid_sig = base64.b64decode(
        'qzVgS1V+kTYrtMqQjq9tpbzgJKdyXG8wTU2oZgCEyV10RmRkZgJPN/WPRnvJzGR7Gpl5Q4bnTvchE+3/Rt6jMQ=='
    )
    valid_public_key = base64.b64decode(
        'AhyFMVWpIpg/LJOKSSsaemB8mPQL5yBlBVER6QuoelVO'
    )
    tx.apply_sig(valid_sig, uncompress_key(valid_public_key))
    assert valid_tx == tx.encode()
    tx.remove_sig()
    print(tx.signing_json())
    assert verify_sig(uncompress_key(valid_public_key), tx.signing_hash(), valid_sig), 'Wrong json encoding'
