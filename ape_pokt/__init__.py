from ape import plugins

from .providers import PoktEthereumProvider

NETWORKS = [
    "mainnet",
    "ropsten",
    "rinkeby",
    "goerli",
]


@plugins.register(plugins.ProviderPlugin)
def providers():
    for network_name in NETWORKS:
        yield "ethereum", network_name, PoktEthereumProvider
