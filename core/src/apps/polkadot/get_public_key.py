from trezor import ui
from trezor.messages import ButtonRequestType
from trezor.messages.PolkadotPublicKey import PolkadotPublicKey
from trezor.ui.text import Text
from trezor.utils import chunks

from apps.common import paths, seed
from apps.common.confirm import require_confirm
from apps.polkadot import CURVE, helpers

from ubinascii import hexlify

async def get_public_key(ctx, msg, keychain):
    # TODO: validate path

    node = keychain.derive(msg.address_n, CURVE)
    pk = seed.remove_ed25519_prefix(node.public_key())
    pk_hex = hexlify(pk).decode()

    if msg.show_display:
        await _show_polkadot_pubkey(ctx, pk_hex)

    return PolkadotPublicKey(public_key=pk_hex)


async def _show_polkadot_pubkey(ctx, pubkey):
    lines = chunks(pubkey, 18)
    text = Text("Confirm public key", ui.ICON_RECEIVE, ui.GREEN)
    text.mono(*lines)
    return await require_confirm(ctx, text, code=ButtonRequestType.PublicKey)
