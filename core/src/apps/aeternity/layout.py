from trezor import ui
from trezor.messages import ButtonRequestType
from trezor.ui.text import Text
from trezor.utils import chunks

from apps.aeternity.helpers import AETERNITY_AMOUNT_DIVISIBILITY, format_amount
from apps.common.confirm import require_confirm, require_hold_to_confirm


async def require_confirm_tx(ctx, recipient, amount):
    text = Text("Confirm sending", ui.ICON_SEND, ui.GREEN)
    text.bold(format_amount(amount))
    text.normal("to")
    text.mono(*split_address(recipient))
    return await require_confirm(ctx, text, ButtonRequestType.SignTx)


async def require_confirm_fee(ctx, amount, fee):
    text = Text("Confirm transaction", ui.ICON_SEND, ui.GREEN)
    text.normal("Type: SpendTx")
    text.normal("Amount:")
    text.bold(format_amount(amount))
    text.normal("Fee:")
    text.bold(format_amount(fee))
    return await require_hold_to_confirm(ctx, text, ButtonRequestType.SignTx)


def split_address(address):
    return chunks(address, 18)
