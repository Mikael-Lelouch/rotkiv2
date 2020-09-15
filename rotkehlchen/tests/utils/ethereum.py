from rotkehlchen.chain.ethereum.manager import NodeName

ETHEREUM_TEST_PARAMETERS = ['ethrpc_endpoint,ethereum_manager_connect_at_start, call_order', [
    # Query etherscan only
    ('', (), (NodeName.ETHERSCAN,)),
    # For "our own" node querying use infura
    (
        'https://mainnet.infura.io/v3/[REDACTED-2026-11-06]',
        (NodeName.OWN,),
        (NodeName.OWN,),
    ),
]]
