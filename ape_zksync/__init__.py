from ape import plugins
from ape.api import create_network_type


@plugins.register(plugins.Config)
def config_class():
    from .config import ZkSyncConfig

    return ZkSyncConfig


@plugins.register(plugins.EcosystemPlugin)
def ecosystems():
    from .ecosystem import ZkSync

    yield ZkSync


@plugins.register(plugins.NetworkPlugin)
def networks():
    from .ecosystem import NETWORKS

    for network_name, (chain_id, network_id) in NETWORKS.items():
        yield "zksync", network_name, create_network_type(chain_id, network_id)


@plugins.register(plugins.ProviderPlugin)
def providers():
    from .ecosystem import NETWORKS
    from .provider import ZkSyncProvider

    for network_name in NETWORKS:
        yield "zksync", network_name, ZkSyncProvider
