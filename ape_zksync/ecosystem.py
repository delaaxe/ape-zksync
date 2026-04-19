from ape_ethereum.ecosystem import Ethereum

from .config import ZkSyncConfig

# zkSync Era network chain IDs
NETWORKS = {
    # network_name: (chain_id, network_id)
    "era-sepolia": (300, 300),
    "era-mainnet": (324, 324),
}

# Public RPC endpoints (user can override in ape-config.yaml)
DEFAULT_RPC = {
    "era-sepolia": "https://sepolia.era.zksync.dev",
    "era-mainnet": "https://mainnet.era.zksync.io",
}


class ZkSync(Ethereum):
    @property
    def config(self) -> ZkSyncConfig:  # type: ignore
        return self.config_manager.get_config("zksync")  # type: ignore
