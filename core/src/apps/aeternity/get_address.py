from trezor.crypto import hashlib
from trezor.messages.AeternityAddress import AeternityAddress

from apps.aeternity import CURVE, helpers
from apps.common import paths, seed
from apps.common.layout import address_n_to_str, show_address, show_qr


async def get_address(ctx, msg, keychain):
    # TODO: validate path

    node = keychain.derive(msg.address_n, CURVE)

    pk = seed.remove_ed25519_prefix(node.public_key())
    # pkh = hashlib.blake2b(pk, outlen=20).digest()
    address = helpers.base58_encode_check_prepend(
        pk, prefix=helpers.AETERNITY_ACCOUNT_PREFIX
    )

    if msg.show_display:
        desc = address_n_to_str(msg.address_n)
        while True:
            if await show_address(ctx, address, desc=desc):
                break
            if await show_qr(ctx, address, desc=desc):
                break

    return AeternityAddress(address=address)
