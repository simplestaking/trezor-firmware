from trezor import wire
from trezor.messages import MessageType

from apps.common import HARDENED

CURVE = "ed25519"


def boot():
    ns = [[CURVE, HARDENED | 44, HARDENED | 1729]]
    wire.add(MessageType.TezosGetAddress, __name__, "get_address", ns)
    wire.add(MessageType.TezosSignTx, __name__, "sign_tx", ns)
    wire.add(MessageType.TezosGetPublicKey, __name__, "get_public_key", ns)
    wire.add(MessageType.TezosSignDelegatorOp, __name__, "sign_delegator_op", ns)
    wire.add(MessageType.TezosControlStaking, __name__, "control_staking")
