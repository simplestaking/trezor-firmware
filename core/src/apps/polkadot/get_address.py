from trezor.crypto import hashlib
from trezor.crypto import base58
from trezor.messages.PolkadotAddress import PolkadotAddress

from apps.common import paths, seed
from apps.common.layout import address_n_to_str, show_address, show_qr
from apps.polkadot import CURVE, helpers


async def get_address(ctx, msg, keychain):
    # TODO: validate path

    node = keychain.derive(msg.address_n, CURVE)
    pk = seed.remove_ed25519_prefix(node.public_key())

    # add address prefix to public key
    pk = bytearray([42]) + pk

    # add SS8 prefix to the public key (this is the input for the blake2 hash function)
    to_hash = b'SS58PRE' + pk

    # get the blake2 hash and append the first 2 bytes as checksum to the address
    pkh = hashlib.blake2b(bytes(to_hash)).digest()
    final = pk + pkh[:2]

    # encode the address
    address = base58.encode(bytes(final))

    if msg.show_display:
        desc = address_n_to_str(msg.address_n)
        while True:
            if await show_address(ctx, address, desc=desc):
                break
            if await show_qr(ctx, address, desc=desc):
                break

    return PolkadotAddress(address=address)
