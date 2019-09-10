from trezorlib import ui, cosmos, messages
from trezorlib.client import TrezorClient
from trezorlib.protobuf import dict_to_proto
from trezorlib.tools import parse_path
from trezorlib.transport import get_transport
import base64
import json
import subprocess


def trezor_connect():
    transport = get_transport()
    return TrezorClient(transport, ui=ui.ClickUI())


def hex_to_base64(hex_string) -> str:
    return base64.b64encode(bytes.fromhex(hex_string)).decode('utf-8')


client = trezor_connect()

path = parse_path("m/44'/118'/0'")
address = cosmos.get_address(client, path)

outp = subprocess.Popen(['gaiacli', 'query', 'account', address, '--output', 'json'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
account_info, stderr = outp.communicate()
# print(account_info.decode('utf-8'))
account_info = json.loads(account_info)

tx_to_sign = {
    "account_number": account_info['value']['account_number'],
    "chain_id": "gaia-13006",
    "fee": {
        "amount": {
            "amount": 0,
            "denom": "muon",
        },
        "gas": 200000,
    },
    "memo": "",
    "msgs": {
        "type": "cosmos-sdk/MsgSend",
        "amount": {
            "amount": 1000,
            "denom": "muon",
        },
        "from_address": "cosmos1evwx7u5xllw5fvyl6wpkmqszl6ql6ta8xd06rn",
        "to_address": "cosmos1u4jc75qlrk2tsjak2leqngh6yvxrlca8ateprj",
    },
    "sequence": account_info['value']['sequence']
}

msg = dict_to_proto(messages.CosmosSignTx, tx_to_sign)
signature = cosmos.sign_tx(client, path, msg)

pub_key = cosmos.get_public_key(client, path)

gaiacli_tx = {
    "type": "cosmos-sdk/StdTx",
    "value": {
        "msg": [
            {
                "type": tx_to_sign['msgs']['type'],
                "value": {
                    "from_address": tx_to_sign['msgs']['from_address'],
                    "to_address": tx_to_sign['msgs']['to_address'],
                    "amount": [{"denom": "muon", "amount": str(tx_to_sign["msgs"]['amount']['amount'])}],
                }
            }
        ],
        "fee": {
            "amount": [],
            "gas": str(tx_to_sign['fee']['gas']),
        },
        "signatures": [
            {
                "signature": base64.b64encode(signature.signature).decode('utf-8'),
                "pub_key": {"type": "tendermint/PubKeySecp256k1", "value": hex_to_base64(pub_key.public_key_hex)},
            }
        ],
        "memo": ""
    }
}


# print(signature.signature)
# b64_signarure = base64.b64encode(signature.signature).decode('utf-8')

# print(b64_signarure)

# print('\nGAIACLI:\n')
pushable = json.dumps(gaiacli_tx, separators=(",", ":"))
with open('tx_data.json', 'w') as outfile:
    json.dump(gaiacli_tx, outfile)
out = subprocess.Popen(['gaiacli', 'tx', 'broadcast', "tx_data.json", '--output', 'json'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout, err = out.communicate()
print(stdout.decode('utf-8'))
