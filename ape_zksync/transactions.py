from typing import List

import rlp  # type: ignore


def rlp_encode_hex(fields: List) -> str:
    serialized = rlp.encode(
        [bytes.fromhex(field[2:]) if isinstance(field, str) else field for field in fields]
    )
    return f"0x{serialized.hex()}"


def serialize_eip712_transaction(transaction: dict) -> str:
    # Ported from: https://www.npmjs.com/package/zksync-web3
    # Source code not on GitHub, but can be seen once installed in:
    # node_modules/zksync-web3/src/utils.ts, function serialize()

    assert transaction["type"] in [113, "0x71"], "not eip712"

    max_fee_per_erg = transaction["gasPrice"]
    max_priority_fee_per_erg = max_fee_per_erg

    fields = [
        transaction["nonce"],
        max_priority_fee_per_erg,
        max_fee_per_erg,
        transaction["gasLimit"],
        transaction["to"],
        transaction["value"],
        transaction["data"],
    ]

    # no EOA signature here
    fields += [
        transaction["chainId"],
        "0x",
        "0x",
        transaction["chainId"],
        transaction["from"],
        "0x027100",  # DEFAULT_ERGS_PER_PUBDATA_LIMIT
        [],  # factory deps
        transaction["customData"]["customSignature"],
        [],  # paymaster params
    ]

    serialized = rlp_encode_hex(fields)
    return f"0x71{serialized[2:]}"
