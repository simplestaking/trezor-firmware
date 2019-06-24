# Automatically generated by pb2py
# fmt: off
import protobuf as p

if __debug__:
    try:
        from typing import List
    except ImportError:
        List = None  # type: ignore


class LibraAddress(p.MessageType):
    MESSAGE_WIRE_TYPE = 801

    def __init__(
        self,
        address: List[int] = None,
    ) -> None:
        self.address = address if address is not None else []

    @classmethod
    def get_fields(cls):
        return {
            1: ('address', p.UVarintType, p.FLAG_REPEATED),
        }
