from trezor.crypto import hashlib
from trezor.messages.LibraAddress import LibraAddress

from apps.common import paths, seed
from apps.common.layout import address_n_to_str, show_address, show_qr
from apps.libra import CURVE

from ubinascii import hexlify


async def get_address(ctx, msg, keychain):
    # TODO: validate the path

    node = keychain.derive(msg.address_n, CURVE)

    # libra addresses look like this:
    # f6dfb3f0df072a2739fd67f1bed449692b47c5acb7db208a4e1faaa6da5263e6

    # get the pk
    pk = seed.remove_ed25519_prefix(node.public_key())
    pkh = hexlify(hashlib.sha3_256(pk, keccak=True).digest()).decode()

    print(pkh)

    # show it on display
    if msg.show_display:
        desc = address_n_to_str(msg.address_n)
        while True:
            if await show_address(ctx, pkh, desc=desc):
                break
            if await show_qr(ctx, hexlify(pkh), desc=desc):
                break

    # return the LibraPublicKey message
    return LibraAddress(address=hexlify(pkh))
