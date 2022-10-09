from typing import List

import rlp


def rlp_encode_hex(fields: List[str]) -> str:
    assert all(field[:2] == "0x" for field in fields), "only supports 0x-prefixed hex strings"
    serialized = rlp.encode([bytes.fromhex(value[2:]) for value in fields])
    return f"0x{serialized.hex()}"
