# Automatically generated by pb2py
# fmt: off
import protobuf as p

from .Amount import Amount

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class Fee(p.MessageType):

    def __init__(
        self,
        amount: Amount = None,
        gas: int = None,
    ) -> None:
        self.amount = amount
        self.gas = gas

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('amount', Amount, 0),
            2: ('gas', p.UVarintType, 0),
        }
