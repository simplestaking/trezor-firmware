from trezor import config, wire
from trezor.messages.Failure import Failure
from trezor.messages.Success import Success
from trezor.pin import pin_to_int

from apps.common.request_pin import request_pin
from apps.tezos import helpers, layout


async def control_baking(ctx, msg):
    if not config.has_pin():
        return Failure()

    if msg.baking is True:
        if not wire.is_baking():
            await layout.require_confirm_baking(ctx)
            wire.tezos_remove_handelrs()
            return Success(message="Baking mode activated")
        else:
            return Success(message="Trezor is already in baking mode")
