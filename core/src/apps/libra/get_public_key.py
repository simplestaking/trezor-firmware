from trezor import ui
from trezor.messages import ButtonRequestType
from trezor.messages.LibraPublicKey import LibraPublicKey
from trezor.ui.text import Text
from trezor.utils import chunks

from apps.common import paths, seed
from apps.common.confirm import require_confirm
from apps.libra import CURVE

from ubinascii import hexlify


async def get_public_key(ctx, msg, keychain):
    # TODO: validate path

    node = keychain.derive(msg.address_n, CURVE)
    pk = hexlify(seed.remove_ed25519_prefix(node.public_key())).decode()
    print(pk)

    if msg.show_display:
        await _show_libra_pubkey(ctx, pk)

    return LibraPublicKey(public_key=pk)


# TODO: move to layout
async def _show_libra_pubkey(ctx, pubkey):
    lines = chunks(pubkey, 18)
    text = Text("Confirm public key", ui.ICON_RECEIVE, ui.GREEN)
    text.mono(*lines)
    return await require_confirm(ctx, text, code=ButtonRequestType.PublicKey)
