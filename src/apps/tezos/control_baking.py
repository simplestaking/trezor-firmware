from trezor import config
from trezor.messages.Failure import Failure
from trezor.messages.Success import Success
from trezor.pin import pin_to_int

from apps.common.request_pin import request_pin
from apps.tezos import helpers, layout


async def control_baking(ctx, msg):

    if not config.has_pin():
        await layout.no_pin_dialog(ctx)
        return Failure()

    if msg.baking is True:
        if not helpers.check_baking_confirmed():
            await layout.require_confirm_baking(ctx)
            helpers.set_baking_state(True)
        else:
            return Success(message="Trezor is already in staking mode")
    else:
        if helpers.check_baking_confirmed():
            await helpers.prompt_pin()
            helpers.set_baking_state(False)
        else:
            return Success(message="Trezor not in staking mode")

    return Success()
