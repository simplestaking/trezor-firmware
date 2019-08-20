from trezor import ui
from trezor.messages import ButtonRequestType
from trezor.ui.text import Text
from trezor.utils import chunks, format_amount

from apps.common.confirm import require_confirm, require_hold_to_confirm
from apps.polkadot import helpers


async def require_confirm_tx(ctx, to, value):
    text = Text("Confirm sending", ui.ICON_SEND, ui.GREEN)
    text.bold('{} miliDOT'.format(value // pow(10, 12)))
    text.normal("to")
    text.mono(*split_address(helpers.ss58_encode(to)))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


def split_address(address):
    return chunks(address, 16)

