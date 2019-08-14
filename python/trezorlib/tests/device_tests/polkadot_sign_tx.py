from trezorlib import messages, ui, polkadot
from trezorlib.client import TrezorClient
from trezorlib.protobuf import dict_to_proto
from trezorlib.tools import parse_path
from trezorlib.transport import get_transport


def trezor_connect():
    transport = get_transport()
    return TrezorClient(transport, ui=ui.ClickUI())


client = trezor_connect()

path = parse_path("m/44'/357'/1'")
print(polkadot.get_address(client, path))

msg = dict_to_proto(messages.PolkadotSignTx, {
    "era": "00",
    "nonce": 0x01,
    "tip": 0x00,
    "checkpoint_hash": "dcd1346701ca8396496e52aa2785b1748deb6db09551b72159dcb3e08991025b",
    "transfer": {
        "module_index": 0x05,
        "call_index": 0x00,
        "destination": "2c31ede147b6ba608a5f89bf218cb9962914895980b1881a4e4b7bd3a0faa2a6",
        "value": 0x01
    }
})

signed = polkadot.sign_tx(client, path, msg)

print(signed.signature)
