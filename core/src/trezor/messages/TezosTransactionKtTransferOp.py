# Automatically generated by pb2py
# fmt: off
import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class TezosTransactionKtTransferOp(p.MessageType):

    def __init__(
        self,
        amount: int = None,
        recipient: bytes = None,
    ) -> None:
        self.amount = amount
        self.recipient = recipient

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('amount', p.UVarintType, 0),
            2: ('recipient', p.BytesType, 0),
        }
