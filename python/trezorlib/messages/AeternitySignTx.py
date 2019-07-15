# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List, Optional
    except ImportError:
        Dict, List, Optional = None, None, None  # type: ignore


class AeternitySignTx(p.MessageType):
    MESSAGE_WIRE_TYPE = 804

    def __init__(
        self,
        address_n: List[int] = None,
        vsn: int = None,
        sender_id: bytes = None,
        recipient_id: bytes = None,
        amount: int = None,
        fee: int = None,
        ttl: int = None,
        nonce: int = None,
        payload: bytes = None,
    ) -> None:
        self.address_n = address_n if address_n is not None else []
        self.vsn = vsn
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.amount = amount
        self.fee = fee
        self.ttl = ttl
        self.nonce = nonce
        self.payload = payload

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('address_n', p.UVarintType, p.FLAG_REPEATED),
            2: ('vsn', p.UVarintType, 0),
            3: ('sender_id', p.BytesType, 0),
            4: ('recipient_id', p.BytesType, 0),
            5: ('amount', p.UVarintType, 0),
            6: ('fee', p.UVarintType, 0),
            7: ('ttl', p.UVarintType, 0),
            8: ('nonce', p.UVarintType, 0),
            9: ('payload', p.BytesType, 0),
        }
