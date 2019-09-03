from micropython import const

from trezor import wire
from trezor.crypto import hashlib
from trezor.crypto.curve import ed25519
from trezor.messages import TezosBallotType, TezosContractType
from trezor.messages.TezosSignedTx import TezosSignedTx

from apps.common import paths
from apps.common.writers import write_bytes, write_uint8, write_uint32_be
from apps.cosmos import CURVE, helpers, layout


async def sing_tx(ctx, msg, keychain):

    node = keychain.derive(msg.address_n, CURVE)

    