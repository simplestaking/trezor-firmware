# Automatically generated by pb2py
# fmt: off
import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class AeternitySignedTx(p.MessageType):
    MESSAGE_WIRE_TYPE = 805

    def __init__(
        self,
        signature: str = None,
        raw_bytes: bytes = None,
    ) -> None:
        self.signature = signature
        self.raw_bytes = raw_bytes

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('signature', p.UnicodeType, 0),
            2: ('raw_bytes', p.BytesType, 0),
        }
