from ape_zksync.transactions import rlp_encode_hex


def test_basic_fields_rlp():
    serialized = rlp_encode_hex(
        [
            "0x",
            "0x05f5e100",
            "0x05f5e100",
            "0x072f42",
            "0xfc070626B677a62521d37519D341E9493b2d83f5",
            "0x",
            "0x3fb5c1cb0000000000000000000000000000000000000000000000000000000000000045",
        ]
    )
    expected = "0xf84a808405f5e1008405f5e10083072f4294fc070626b677a62521d37519d341e9493b2d83f580a43fb5c1cb0000000000000000000000000000000000000000000000000000000000000045"  # noqa: E501
    assert serialized == expected
