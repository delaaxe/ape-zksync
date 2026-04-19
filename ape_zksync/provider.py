from typing import Optional

from ape.api import ReceiptAPI, TransactionAPI
from ape.exceptions import ProviderError
from ape_ethereum.provider import Web3Provider
from web3 import HTTPProvider, Web3

from .ecosystem import DEFAULT_RPC


class ZkSyncProvider(Web3Provider):
    """
    Ape provider for zkSync Era networks.

    Uses Web3Provider (pure HTTP) — no geth dependency.
    zkSync Era is EVM-compatible: standard eth_* calls work for reads,
    deploys, and EOA transactions. Type 113 (EIP-712 / paymaster)
    transactions are a future extension.
    """

    @property
    def connection_str(self) -> str:
        return self.uri

    @property
    def uri(self) -> str:
        ecosystem_cfg = self.config_manager.get_config("zksync")
        network_key = self.network.name.replace("-", "_")
        network_cfg = getattr(ecosystem_cfg, network_key, None)
        if network_cfg and getattr(network_cfg, "uri", None):
            return network_cfg.uri
        return DEFAULT_RPC.get(self.network.name, DEFAULT_RPC["era-sepolia"])

    def connect(self) -> None:
        self._web3 = Web3(HTTPProvider(self.uri))
        if not self._web3.is_connected():
            raise ProviderError(f"Could not connect to zkSync Era at {self.uri}")
        chain_id = self._web3.eth.chain_id
        expected = self.network.chain_id
        if chain_id != expected:
            raise ProviderError(
                f"Connected to chain {chain_id}, expected {expected} "
                f"for {self.network.name}. Check your RPC URI."
            )

    def disconnect(self) -> None:
        self._web3 = None

    def get_zksync_l1_batch_number(self) -> Optional[int]:
        """Return the current L1 batch number — useful for gas comparison demos."""
        try:
            result = self.web3.provider.make_request("zks_L1BatchNumber", [])
            return int(result["result"], 16)
        except Exception:
            return None

    def get_zksync_main_contract(self) -> Optional[str]:
        """Return the zkSync diamond proxy address on L1."""
        try:
            result = self.web3.provider.make_request("zks_getMainContract", [])
            return result.get("result")
        except Exception:
            return None
