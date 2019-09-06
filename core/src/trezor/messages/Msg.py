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


class Msg(p.MessageType):

    def __init__(
        self,
        type: str = None,
        from_address: str = None,
        to_address: str = None,
        amount: Amount = None,
    ) -> None:
        self.type = type
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('type', p.UnicodeType, 0),
            2: ('from_address', p.UnicodeType, 0),
            3: ('to_address', p.UnicodeType, 0),
            4: ('amount', Amount, 0),
        }
