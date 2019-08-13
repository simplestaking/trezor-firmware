from trezorlib import messages, ui, polkadot
from trezorlib.client import TrezorClient
from trezorlib.protobuf import dict_to_proto
from trezorlib.tools import parse_path
from trezorlib.transport import get_transport


def trezor_connect():
    transport = get_transport()
    return TrezorClient(transport, ui=ui.ClickUI())


client = trezor_connect()

path = parse_path("m/44'/357'/0'/0'/0'")

msg = dict_to_proto(messages.PolkadotSignTx, {
    "era": 0x20,
    "nonce": 0x1,
    "tip": 0x00,
    "checkpoint_hash": "2e2d",
    "transfer": {
        "module_index": 0x5,
        "call_index": 0x0,
        "dest": "1111",
        "value": 0x01
    }
})

signed = polkadot.sign_tx(client, path, msg)

print(signed.signature)
