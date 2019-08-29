from trezorlib import ui, cosmos
from trezorlib.client import TrezorClient
# from trezorlib.protobuf import dict_to_proto
from trezorlib.tools import parse_path
from trezorlib.transport import get_transport


def trezor_connect():
    transport = get_transport()
    return TrezorClient(transport, ui=ui.ClickUI())


client = trezor_connect()

path = parse_path("m/44'/118'/0'")

address = cosmos.get_address(client, path)
pub_key = cosmos.get_public_key(client, path)

print(address)
print(pub_key)
