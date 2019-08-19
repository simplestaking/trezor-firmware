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
sender = polkadot.get_public_key(client, path)

msg_dict = {
    "era": "00",
    "nonce": 0x01,
    "tip": 0x00,
    "genesis_hash": "dcd1346701ca8396496e52aa2785b1748deb6db09551b72159dcb3e08991025b",
    # "block_hash": "9b0e498c1e77204f7718ac7d8efa6b89ba550f1bbd0915e09536641ff40b219e",
    "transfer": {
        "module_index": 0x03,
        "call_index": 0x00,
        "destination": "2c31ede147b6ba608a5f89bf218cb9962914895980b1881a4e4b7bd3a0faa2a6",
        "value": 3000000000000
    }
}

msg = dict_to_proto(messages.PolkadotSignTx, msg_dict)

signed = polkadot.sign_tx(client, path, msg)

transaction = '0x390281ff' \
              + sender \
              + signed.signature \
              + signed.encoded_nonce \
              + msg_dict['era']\
              + '0300ff' \
              + msg_dict['transfer']['destination'] \
              + signed.encoded_value

print('Signature in hex format: 0x' + signed.signature)
print('Balance transfer extrinsic: ' + transaction)
