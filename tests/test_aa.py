import pytest

from ape_zksync.transactions import rlp_encode_hex, serialize_eip712_transaction


def test_rlp_encoding():
    fields = [
        "0x",
        "0x05f5e100",
        "0x05f5e100",
        "0x072f42",
        "0xfc070626B677a62521d37519D341E9493b2d83f5",
        "0x",
        "0x3fb5c1cb0000000000000000000000000000000000000000000000000000000000000045",
    ]

    serialized = rlp_encode_hex(fields)
    expected = "0xf84a808405f5e1008405f5e10083072f4294fc070626b677a62521d37519d341e9493b2d83f580a43fb5c1cb0000000000000000000000000000000000000000000000000000000000000045"  # noqa: E501

    assert serialized == expected


def test_eip712_transaction_serialization():
    transaction = {
        "type": "0x71",
        "to": "0x1A7572122C726Fb2EFe1a0070D09c2Cd48FB4A05",
        "from": "0x4F7D08D197E8e8B391F2a7d832934163575D7a4C",  # <-- SMART CONTRACT
        "data": "0x3fb5c1cb0000000000000000000000000000000000000000000000000000000000000045",
        "value": "0x",
        "chainId": "0x0118",
        "gasPrice": "0x05f5e100",
        "gasLimit": "0x072f42",
        "nonce": "0x",
        "customData": {  # customSignature is "multisig"
            "customSignature": "0xffe882acd2daf21a9688e627d791730a1d9655fb379f9b0710dc5f2dcc3db0a46978b49f7af25cb0716b3f0d3cb6a9d9d984d2188dc0195537a2cac381cd785b1b572c86c86e908e3d6f8f7d3f5c9685037f36d06b89ae77cb4f65807628d79baa15e491eaee759d4f1507dd3613c12a3b7b45749976a98fc702b99c12a114da701c"  # noqa: E501
        },
    }

    serialized = serialize_eip712_transaction(transaction)
    expected = "0x71f8f1808405f5e1008405f5e10083072f42941a7572122c726fb2efe1a0070d09c2cd48fb4a0580a43fb5c1cb00000000000000000000000000000000000000000000000000000000000000458201188080820118944f7d08d197e8e8b391f2a7d832934163575d7a4c83027100c0b882ffe882acd2daf21a9688e627d791730a1d9655fb379f9b0710dc5f2dcc3db0a46978b49f7af25cb0716b3f0d3cb6a9d9d984d2188dc0195537a2cac381cd785b1b572c86c86e908e3d6f8f7d3f5c9685037f36d06b89ae77cb4f65807628d79baa15e491eaee759d4f1507dd3613c12a3b7b45749976a98fc702b99c12a114da701cc0"  # noqa: E501

    assert serialized == expected


@pytest.mark.skip(reason="transaction already sent")
def test_eip712_transaction_sending(provider_context):
    with provider_context as zksync_provider:
        serialized = "0x71f8f1808405f5e1008405f5e10083072f42948cdd29ebfed75af28acba4441be77201056d800980a43fb5c1cb00000000000000000000000000000000000000000000000000000000000000458201188080820118942d81a9c7718797c746e4fddeecbb1982b2982cca83027100c0b8826a75c3135ff75bb3939e7d947c2bbb7aa91e14d07e5b7dae56fad73c9fa84f9300fa1711131e13cf1df6c6e4734f625f18f5473ca8bbe05826b651358e7fde1a1b1107dbdd88a3c41e55cab383b833aa2ea5cc6c5bca93544a2ad3df67818c4c9315254054a31783e28fd0c2707a508477b393efd968405e5841af9cfc98a9f9c61cc0"  # noqa: E501
        txn_hash = zksync_provider.web3.eth.send_raw_transaction(bytes.fromhex(serialized[2:]))
        print("hash", txn_hash)
        # AA transaction confirmed here:
        # https://explorer.zksync.io/tx/0x07ce8617c81410abfb304f4af8e6cdc4948ff58006126a9981c05fa82d69c22f
