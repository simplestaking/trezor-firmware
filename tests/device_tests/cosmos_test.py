from trezorlib import ui, cosmos, messages
from trezorlib.client import TrezorClient
from trezorlib.protobuf import dict_to_proto
from trezorlib.tools import parse_path
from trezorlib.transport import get_transport


def trezor_connect():
    transport = get_transport()
    return TrezorClient(transport, ui=ui.ClickUI())


client = trezor_connect()

path = parse_path("m/44'/118'/0'")

tx = {
    "account_number": 11335,
    "chain_id": "cosmoshub-2",
    "fee": {
        "amount": {
            "amount": 1000,
            "denom": "uatom",
        },
        "gas": 37000,
    },
    "memo": "",
    "msgs": {
        "type": "cosmos-sdk/MsgSend",
        "amount": {
            "amount": 387000,
            "denom": "uatom",
        },
        "from_address": "cosmos1lgharzgds89lpshr7q8kcmd2esnxkfpwvuz5tr",
        "to_address": "cosmos103l758ps7403sd9c0y8j6hrfw4xyl70j4mmwkf",
    },
    "sequence": 0
}

msg = dict_to_proto(messages.CosmosSignTx, tx)

# address = cosmos.get_address(client, path)
# pub_key = cosmos.get_public_key(client, path)

# print(address)
# print(pub_key)

signature = cosmos.sign_tx(client, path, msg)
print(signature)
