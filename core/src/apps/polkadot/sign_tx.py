from micropython import const

from trezor import wire
from trezor.crypto import hashlib
from trezor.crypto.curve import ed25519
from trezor.messages.PolkadotSignedTx import PolkadotSignedTx

from apps.common import paths
from apps.common.writers import write_bytes, write_uint8, write_uint64_le, write_uint128_le
from apps.polkadot import helpers, CURVE
from ubinascii import hexlify
from trezor.crypto import bip39

async def sign_tx(ctx, msg, keychain):

    node = keychain.derive(msg.address_n, CURVE)

    seed = bip39.seed('all all all all all all all all all all all all', "m'/357'/0'")
    print('SEED: ' + hexlify(seed).decode())

    w = bytearray()

    # debug
    z = bytearray()
    helpers.scale_int_encode(z, 142)
    print('Nonce: ' + hexlify(z).decode())

    method_len = len(msg.transfer.destination) + 3 + helpers.get_byte_count(msg.transfer.value)

    # signing for Alexander network
    helpers.scale_int_encode(w, msg.nonce)
    # helpers.scale_int_encode(w, method_len)
    write_uint8(w, msg.transfer.module_index)
    write_uint8(w, msg.transfer.call_index)
    write_bytes(w, helpers.scale_encode_address(msg.transfer.destination))
    helpers.scale_int_encode(w, msg.transfer.value)
    write_bytes(w, msg.era)

    # helpers.scale_int_encode(w, msg.tip)

    # immortal
    if msg.genesis_hash:
        write_bytes(w, msg.genesis_hash)
    # mortal
    if msg.block_hash:
        write_bytes(w, msg.block_hash)

    signature = ed25519.sign(node.private_key(), w)
    hex_sig = hexlify(signature).decode()

    hex_data = hexlify(w).decode()
    print('SIGNED DATA: ' + hex_data)

    return PolkadotSignedTx(signature=hex_sig)

