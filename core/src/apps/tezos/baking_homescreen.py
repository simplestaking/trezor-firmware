from trezor import ui, loop, io
from trezor.ui.text import Text

from apps.tezos import helpers


async def baking_homescreen():
    # render homescreen in dimmed mode and fade back in
    await ui.backlight_slide(ui.BACKLIGHT_DIM)
    display_baking_homescreen()
    await ui.backlight_slide(ui.BACKLIGHT_NORMAL)

    # loop forever, never return
    touch = loop.wait(io.TOUCH)
    while True:
        await touch


def display_baking_homescreen():
    ui.display.clear()

    # TODO - fix the overlapping bar
    ui.display.bar(0, 0, ui.WIDTH, 30, ui.GREEN)
    ui.display.text_center(
        ui.WIDTH // 2, 22, "TEZOS BAKING", ui.BOLD, ui.WHITE, ui.GREEN
    )
    ui.display.bar(0, 30, ui.WIDTH, ui.HEIGHT - 30, ui.BG)

    text = Text("Last Operation", ui.ICON_SEND, icon_color=ui.GREEN)
    text.normal("")
    text.bold("Level:")
    text.normal(str(helpers.get_last_level()))
    text.bold("Type:")
    text.normal(helpers.get_last_type())
    text.render()
    ui.display.backlight(ui.BACKLIGHT_NORMAL)
