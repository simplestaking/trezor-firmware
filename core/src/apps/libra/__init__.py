from trezor import wire
from trezor.messages import MessageType

from apps.common import HARDENED

CURVE = "ed25519"


def boot():
    ns = [[CURVE, HARDENED | 44, HARDENED | 55555]]
    wire.add(MessageType.LibraGetAddress, __name__, "get_address", ns)
    wire.add(MessageType.LibraGetPublicKey, __name__, "get_public_key", ns)
