# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
        from typing_extensions import Literal  # noqa: F401
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class TezosTransactionOpLegacyDelegation(p.MessageType):

    def __init__(
        self,
        delegate: str = None,
    ) -> None:
        self.delegate = delegate

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('delegate', p.UnicodeType, 0),
        }
