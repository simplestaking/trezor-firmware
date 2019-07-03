from trezor import wire
from trezor.messages import MessageType

from apps.common import HARDENED

CURVE = "ed25519"


def boot():
    # note: the value '55555' is arbitrary, we should use the slip 44 value (not yet registered)
    ns = [[CURVE, HARDENED | 44, HARDENED | 55555]]
    wire.add(MessageType.LibraGetAddress, __name__, "get_address", ns)
    wire.add(MessageType.LibraGetPublicKey, __name__, "get_public_key", ns)
    wire.add(MessageType.LibraSignTx, __name__, "sign_tx", ns)
