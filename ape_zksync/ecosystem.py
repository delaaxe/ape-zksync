from typing import Dict, List, Optional

from ape.api import BlockAPI, ReceiptAPI, TransactionAPI
from ape.api.config import PluginConfig
from ape_ethereum.ecosystem import Block, Ethereum, NetworkConfig
from ape_ethereum.transactions import Receipt, TransactionStatusEnum
from hexbytes import HexBytes

NETWORKS = {
    # chain_id, network_id
    "goerli": (280, 280),
}


class ZkSyncConfig(PluginConfig):
    goerli: NetworkConfig = NetworkConfig(required_confirmations=1, block_time=1)  # type: ignore
    default_network: str = "goerli"

    # Configure re-mappings using a `=` separated-str,
    # e.g. '@import_name=path/to/dependency'
    import_remapping: List[str] = []
    optimize: bool = True
    version: Optional[str] = None


class ZkSync(Ethereum):
    @property
    def config(self) -> ZkSyncConfig:  # type: ignore
        return self.config_manager.get_config("zksync")  # type: ignore

    def create_transaction(self, **kwargs) -> TransactionAPI:
        """
        Returns a transaction using the given constructor kwargs.
        Returns:
            :class:`~ape.api.transactions.TransactionAPI`
        """
        # TODO: zkSync transactions currently work only with type=0 (non EIP-1559),
        #       so I assume it should be handled here
        return super().create_transaction(**kwargs)

    def decode_receipt(self, data: dict) -> ReceiptAPI:
        status = data.get("status")
        if status:
            if isinstance(status, str) and status.isnumeric():
                status = int(status)

            status = TransactionStatusEnum(status)
        elif status is None:
            print("WARNING: status is None and set to 0")
            status = 1  # HACK: it seems status can be None on zkSync so using this hack

        txn_hash = data.get("hash")

        if txn_hash:
            txn_hash = data["hash"].hex() if isinstance(data["hash"], HexBytes) else data["hash"]

        if data.get("data") and isinstance(data.get("data"), str):
            data["data"] = bytes(HexBytes(data.get("data")))  # type: ignore

        elif data.get("input", b"") and isinstance(data.get("input", b""), str):
            data["input"] = bytes(HexBytes(data.get("input", b"")))

        receipt = Receipt(  # type: ignore
            block_number=data.get("block_number")
            or data.get("blockNumber")
            or 999,  # HACK: can be None
            contract_address=data.get("contractAddress"),
            gas_limit=data.get("gas") or data.get("gasLimit") or 999,  # HACK: can be None
            gas_price=data.get("gas_price") or data.get("gasPrice"),
            gas_used=data.get("gas_used") or data.get("gasUsed"),
            logs=data.get("logs", []),
            status=status,
            txn_hash=txn_hash,
            transaction=self.create_transaction(**data),
        )
        return receipt

    def decode_block(self, data: Dict) -> BlockAPI:
        data["hash"] = HexBytes(data["hash"]) if data.get("hash") else None
        if "gas_limit" in data:
            data["gasLimit"] = data.pop("gas_limit")
        if "gas_used" in data:
            data["gasUsed"] = data.pop("gas_used")
        if "parent_hash" in data:
            data["parentHash"] = HexBytes(data.pop("parent_hash"))
        if "transaction_ids" in data:
            data["transactions"] = data.pop("transaction_ids")
        if "total_difficulty" in data:
            data["totalDifficulty"] = data.pop("total_difficulty")
        if "base_fee" in data:
            data["baseFee"] = data.pop("base_fee")
        if "transactions" in data:
            data["num_transactions"] = len(data["transactions"])
        if data.get("totalDifficulty") is None:
            data["totalDifficulty"] = 999  # HACK
        if data.get("size") is None:
            data["size"] = 999  # HACK
        return Block.parse_obj(data)
