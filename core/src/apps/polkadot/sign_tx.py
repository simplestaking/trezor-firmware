from micropython import const

from trezor import wire
from trezor.crypto import hashlib
from trezor.crypto.curve import ed25519
from trezor.messages.PolkadotSignedTx import PolkadotSignedTx

from apps.common import paths
from apps.common.writers import write_bytes, write_uint8, write_uint32_be
from apps.polkadot import helpers
from ubinascii import hexlify

async def sign_tx(ctx, msg, keychain):

    w = bytearray()
    helpers.scale_int_encode(w, 68719476730)
    print(hexlify(w).decode())
    return PolkadotSignedTx(signature="LUL itsa me singaatuure")

