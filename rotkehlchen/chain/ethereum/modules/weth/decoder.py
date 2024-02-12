from typing import TYPE_CHECKING

from rotkehlchen.chain.ethereum.modules.weth.constants import CPT_WETH
from rotkehlchen.chain.evm.decoding.types import CounterpartyDetails
from rotkehlchen.chain.evm.decoding.weth.decoder import WethDecoderBase
from rotkehlchen.constants.assets import A_ETH, A_WETH

if TYPE_CHECKING:
    from rotkehlchen.chain.ethereum.node_inquirer import EthereumInquirer
    from rotkehlchen.chain.evm.decoding.base import BaseDecoderTools
    from rotkehlchen.user_messages import MessagesAggregator


class WethDecoder(WethDecoderBase):
    def __init__(
            self,
            ethereum_inquirer: 'EthereumInquirer',
            base_tools: 'BaseDecoderTools',
            msg_aggregator: 'MessagesAggregator',
    ) -> None:
        super().__init__(
            evm_inquirer=ethereum_inquirer,
            base_tools=base_tools,
            msg_aggregator=msg_aggregator,
            base_asset=A_ETH.resolve_to_crypto_asset(),
            wrapped_token=A_WETH.resolve_to_evm_token(),
            counterparty=CPT_WETH,
        )

    @staticmethod
    def counterparties() -> tuple[CounterpartyDetails, ...]:
        return (CounterpartyDetails(identifier=CPT_WETH, label='WETH', image='weth.svg'),)
