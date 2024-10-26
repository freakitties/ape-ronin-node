from ape.api import PluginConfig
from ape_node import Node
from web3.middleware import geth_poa_middleware
from typing import Dict, Optional
from pathlib import Path
from ape_ronin.ecosystem import NetworkConfig, create_network_config
from ape.logging import logger, sanitize_url

#DEFAULT_SETTINGS = {"uri": "https://api.roninchain.com/rpc"}
#DEFAULT_SETTINGS = {"uri": "https://ronin.lgns.net/rpc"}    #This RPC allows trace_transaction. by default ape_ethereum calls this.

# different than ape_ronin.ecosystem.RoninNetworkConfig i guess. (ref ape_ethereum.ecosystem and ape_node.provider)
class RoninNodeNetworkConfig(PluginConfig):
    mainnet: NetworkConfig = create_network_config(block_time=3, uri="https://api.roninchain.com/rpc")
    saigon: NetworkConfig = create_network_config(block_time=3, uri="https://saigon-testnet.roninchain.com/rpc")
    # Make sure to run via `geth --dev` (or similar)
    #local: Dict = {**DEFAULT_SETTINGS.copy(), "chain_id": DEFAULT_TEST_CHAIN_ID}


class RoninNodeConfig(PluginConfig):
    ronin: RoninNodeNetworkConfig = RoninNodeNetworkConfig()
    executable: Optional[str] = None
    ipc_path: Optional[Path] = None
    data_dir: Optional[Path] = None    


class RoninNode(Node):
    #TODO: set priority_fee post EIP1559
    def _complete_connect(self):
        try:
            super()._complete_connect()            
        except ValueError as ex:
            #Some RPCs (like https://api.roninchain.com/rpc) don't support get_block("first")
            if 'earliest is not a valid block number' in ex.args[0]['message']:
                if geth_poa_middleware not in self._web3.middleware_onion:
                    logger.info("Added POA middleware")
                    self._web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        else:
            logger.info(f"Connected to a '{sanitize_url(self.uri)}'.")


