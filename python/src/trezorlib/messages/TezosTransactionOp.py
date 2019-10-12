# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .TezosContractID import TezosContractID
from .TezosTransactionSmartContractDelegationOp import TezosTransactionSmartContractDelegationOp
from .TezosTransactionSmartContractTransferOp import TezosTransactionSmartContractTransferOp

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class TezosTransactionOp(p.MessageType):

    def __init__(
        self,
        source: bytes = None,
        fee: int = None,
        counter: int = None,
        gas_limit: int = None,
        storage_limit: int = None,
        amount: int = None,
        destination: TezosContractID = None,
        parameters: bytes = None,
        smart_contract_delegation: TezosTransactionSmartContractDelegationOp = None,
        smart_contract_transfer: TezosTransactionSmartContractTransferOp = None,
    ) -> None:
        self.source = source
        self.fee = fee
        self.counter = counter
        self.gas_limit = gas_limit
        self.storage_limit = storage_limit
        self.amount = amount
        self.destination = destination
        self.parameters = parameters
        self.smart_contract_delegation = smart_contract_delegation
        self.smart_contract_transfer = smart_contract_transfer

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            9: ('source', p.BytesType, 0),
            2: ('fee', p.UVarintType, 0),
            3: ('counter', p.UVarintType, 0),
            4: ('gas_limit', p.UVarintType, 0),
            5: ('storage_limit', p.UVarintType, 0),
            6: ('amount', p.UVarintType, 0),
            7: ('destination', TezosContractID, 0),
            8: ('parameters', p.BytesType, 0),
            10: ('smart_contract_delegation', TezosTransactionSmartContractDelegationOp, 0),
            11: ('smart_contract_transfer', TezosTransactionSmartContractTransferOp, 0),
        }
