from trezor.crypto import hashlib
from trezor.crypto import base58
from trezor.messages.PolkadotAddress import PolkadotAddress

from apps.common import paths, seed
from apps.common.layout import address_n_to_str, show_address, show_qr
from apps.polkadot import CURVE, helpers
from ubinascii import hexlify

async def get_address(ctx, msg, keychain):
    # TODO: validate path

    node = keychain.derive(msg.address_n, CURVE)
    pk = seed.remove_ed25519_prefix(node.public_key())

    # Debug
    print(hexlify(pk).decode())

    # TODO: move to helpers
    address = helpers.ss58_encode(pk)

    if msg.show_display:
        desc = address_n_to_str(msg.address_n)
        while True:
            if await show_address(ctx, address, desc=desc):
                break
            if await show_qr(ctx, address, desc=desc):
                break

    return PolkadotAddress(address=address)
