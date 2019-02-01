# Automatically generated by pb2py
# fmt: off
import protobuf as p


class TezosEndorsement(p.MessageType):

    def __init__(
        self,
        branch: bytes = None,
        level: int = None,
    ) -> None:
        self.branch = branch
        self.level = level

    @classmethod
    def get_fields(cls):
        return {
            1: ('branch', p.BytesType, 0),
            2: ('level', p.UVarintType, 0),
        }
