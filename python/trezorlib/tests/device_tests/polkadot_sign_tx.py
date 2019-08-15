from trezorlib import messages, ui, polkadot
from trezorlib.client import TrezorClient
from trezorlib.protobuf import dict_to_proto
from trezorlib.tools import parse_path
from trezorlib.transport import get_transport


def trezor_connect():
    transport = get_transport()
    return TrezorClient(transport, ui=ui.ClickUI())


client = trezor_connect()

path = parse_path("m/44'/357'/0'")
print(polkadot.get_address(client, path))

msg = dict_to_proto(messages.PolkadotSignTx, {
    "era": "00",
    "nonce": 0x04,
    "tip": 0x00,
    "genesis_hash": "dcd1346701ca8396496e52aa2785b1748deb6db09551b72159dcb3e08991025b",
    "transfer": {
        "module_index": 0x03,
        "call_index": 0x00,
        "destination": "2c31ede147b6ba608a5f89bf218cb9962914895980b1881a4e4b7bd3a0faa2a6",
        "value": 3000000000000
    }
})

signed = polkadot.sign_tx(client, path, msg)

print(signed.signature)

# 0x3d02    81  ffddd5ccff603c3801324a92fdb94d160d5efe5c460c491e3aed9117a1b340e69e  b818cbb3703a95fbd32de93d7de4413ff9b4d3c21b8ef55912092cd9e9a2500477cc611ca48c0e054791897af5a049b75c4f3d0357bfbc46f23622072a330a0a    14f502  0300  ffe0ed659d103d939dbbd6b7ac8fe8748c1fbc71b1f1f85bb91c8c44f09a8dc896  0b0030ef7dba02
# 0x3d02    81  ffddd5ccff603c3801324a92fdb94d160d5efe5c460c491e3aed9117a1b340e69e  9452a34d4dd6289106706d058795404a4d9d5f25b8f5767a184e51ea63d7ed8c141632a9dc0653e4305fb1cca396829835e17e163b34520c4323f72c4f20890a    1c9501  0300  ffe0ed659d103d939dbbd6b7ac8fe8748c1fbc71b1f1f85bb91c8c44f09a8dc896  0b0030ef7dba02
# 0300ff2c31ede147b6ba608a5f89bf218cb9962914895980b1881a4e4b7bd3a0faa2a60b0030ef7dba02001000dcd1346701ca8396496e52aa2785b1748deb6db09551b72159dcb3e08991025b