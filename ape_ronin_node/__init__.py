from .provider import RoninNode, RoninNodeConfig

from ape import plugins
from ape.api.networks import LOCAL_NETWORK_NAME, ForkedNetworkAPI, NetworkAPI, create_network_type
from ape_test import LocalProvider
from ape_ronin import NETWORKS

#ecosystem: Ronin
#network: mainnet
#provider: RoninNode

@plugins.register(plugins.Config)
def config_class():
    return RoninNodeConfig

@plugins.register(plugins.ProviderPlugin)
def providers():
    for network_name in NETWORKS:
        yield "ronin", network_name, RoninNode

    #yield "ronin", LOCAL_NETWORK_NAME, LocalProvider

