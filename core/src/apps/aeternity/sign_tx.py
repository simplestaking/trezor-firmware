from micropython import const

from trezor import wire
from trezor.crypto import hashlib
from trezor.crypto.curve import ed25519
from trezor.messages.AeternitySignedTx import AeternitySignedTx

from apps.common import paths
from apps.common.writers import write_bytes, write_uint8, write_uint32_be
from apps.aeternity import CURVE, helpers, layout

if False:
    from trezor.utils import Writer


async def sign_tx(ctx, msg, keychain):
    #TODO: validate path

    node = keychain.derive(msg.address_n, CURVE)

    w = bytearray()

    return AeternitySignedTx(

    )


def _encode_int(w, val: int):
    write_uint_arbitrary_be(w, val)


def _encode_id(w, id_string: str):
    write_uint_arbitrary_be(w, 1)
    write_bytes(w, id_string[3:])
    pass


def get_byte_count(val: int):
    if val < 0:
        return None
    elif val == 0:
        return 1
    elif val > 0:
        count = 0
        while val != 0:
            val >>= 8
            count += 1
        return count


def write_uint_arbitrary_be(w: Writer, n: int) -> int:
    byte_count = get_byte_count(n)

    for i in range(byte_count * 8, 0, -8):
        w.append((n >> i) & 0xFF)

    return byte_count
