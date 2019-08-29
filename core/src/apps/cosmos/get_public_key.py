from trezor import ui
from trezor.messages import ButtonRequestType
from trezor.messages.CosmosPublicKey import CosmosPublicKey
from trezor.ui.text import Text
from trezor.utils import chunks

# from apps.common import paths, seed
from apps.common.confirm import require_confirm
from apps.cosmos import CURVE
from trezor.crypto.bech32 import bech32_encode, convertbits


async def get_public_key(ctx, msg, keychain):
    # TODO: validate path

    node = keychain.derive(msg.address_n, CURVE)
    pk = node.public_key()

    pk = b'0xEB5AE987' + pk
    pk_prefixed = bech32_encode('cosmospub', convertbits(pk, 8, 5))

    if msg.show_display:
        await _show_cosmos_pubkey(ctx, pk_prefixed)

    return CosmosPublicKey(public_key=pk_prefixed)


async def _show_cosmos_pubkey(ctx, pubkey):
    lines = chunks(pubkey, 18)
    text = Text("Confirm public key", ui.ICON_RECEIVE, ui.GREEN)
    text.mono(*lines)
    return await require_confirm(ctx, text, code=ButtonRequestType.PublicKey)
