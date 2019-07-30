from trezor import wire
from trezor.messages import MessageType

from apps.common import HARDENED

CURVE = "ed25519"
# the session key implementation in the Polkadot network. Other account keys use sr25519 not yet supported in trezor

def boot() -> None:
    ns = [[CURVE, HARDENED | 44, HARDENED | 357]]
    wire.add(MessageType.PolkadotGetAddress, __name__, "get_address", ns)
    # wire.add(MessageType.PolkadotSignTx, __name__, "sign_tx", ns)
    wire.add(MessageType.PolkadotGetPublicKey, __name__, "get_public_key", ns)
