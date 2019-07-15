from trezor import wire
from trezor.messages import MessageType

from apps.common import HARDENED

CURVE = "ed25519"


def boot() -> None:
    ns = [[CURVE, HARDENED | 44, HARDENED | 457]]
    wire.add(MessageType.AeternityGetAddress, __name__, "get_address", ns)
    wire.add(MessageType.AeternitySignTx, __name__, "sign_tx", ns)
    wire.add(MessageType.AeternityGetPublicKey, __name__, "get_public_key", ns)
