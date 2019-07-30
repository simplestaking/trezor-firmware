
import namedtupled
from trezorlib import polkadot, messages, ui
from trezorlib.client import TrezorClient
from trezorlib.protobuf import dict_to_proto
from trezorlib.tools import parse_path
from trezorlib.transport import get_transport


def trezor_connect():
    transport = get_transport()
    client = TrezorClient(transport, ui=ui.ClickUI())

    return client


client = trezor_connect()

path = parse_path("m/44'/357'/0'/0'/0'")

address = polkadot.get_address(client, path, show_display=True)

print(address)

# 5E9a7BYEirmsQVwfhVq2eM6RmA4xSJrwnc7UrNGmHGFaZK9d
