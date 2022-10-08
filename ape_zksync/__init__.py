from ape import plugins
from ape.api import create_network_type
from ape_geth import GethProvider

from ape_zksync.compiler import ZkSyncCompiler
from ape_zksync.ecosystem import NETWORKS, ZkSync, ZkSyncConfig


@plugins.register(plugins.Config)
def config_class():
    return ZkSyncConfig


@plugins.register(plugins.EcosystemPlugin)
def ecosystems():
    yield ZkSync


@plugins.register(plugins.NetworkPlugin)
def networks():
    for network_name, network_params in NETWORKS.items():
        yield "zksync", network_name, create_network_type(*network_params)


@plugins.register(plugins.ProviderPlugin)
def providers():
    for network_name in NETWORKS:
        yield "zksync", network_name, GethProvider


@plugins.register(plugins.CompilerPlugin)
def register_compiler():
    return (".sol",), ZkSyncCompiler
