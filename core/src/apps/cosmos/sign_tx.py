from micropython import const

from trezor import wire
from trezor.crypto import hashlib
from trezor.messages.CosmosSignedTx import CosmosSignedTx

from apps.common import paths
from apps.common.writers import write_bytes, write_uint8, write_uint32_be
from apps.cosmos import CURVE, helpers, layout
from trezor.crypto.curve import secp256k1
from ubinascii import hexlify


async def sign_tx(ctx, msg, keychain):

    node = keychain.derive(msg.address_n, CURVE)

    msg_bytes = helpers.construct_json_for_signing(msg)

    encoded = msg_bytes.encode('utf-8')
    h = hashlib.sha256(encoded).digest()
    signature = secp256k1.sign(node.private_key(), h)
    signature_hex = hexlify(signature).decode()

    return CosmosSignedTx(signature=signature_hex)