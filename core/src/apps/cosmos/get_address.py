from trezor.crypto.hashlib import ripemd160, sha256
from trezor.messages.CosmosAddress import CosmosAddress

from apps.common.layout import address_n_to_str, show_address, show_qr

from trezor.crypto.bech32 import bech32_encode, convertbits
from apps.cosmos import CURVE
# from ubinascii import hexlify


async def get_address(ctx, msg, keychain):
    # TODO: validate path

    node = keychain.derive(msg.address_n, CURVE)
    public_key = node.public_key()
    h = sha256(public_key).digest()
    h = ripemd160(h).digest()

    address = bech32_encode('cosmos', convertbits(h, 8, 5))

    if msg.show_display:
        desc = address_n_to_str(msg.address_n)
        while True:
            if await show_address(ctx, address, desc=desc):
                break
            if await show_qr(ctx, address, desc=desc):
                break

    return CosmosAddress(address=address)
