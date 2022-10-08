from ape import plugins
from ape.api import NetworkAPI, create_network_type
from ape.api.networks import LOCAL_NETWORK_NAME
from ape_geth import GethProvider
from ape_test import LocalProvider

from ape_zksync.ecosystem import NETWORKS, ZkSync, ZkSyncConfig
from ape_zksync.compiler import ZkSyncCompiler


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
