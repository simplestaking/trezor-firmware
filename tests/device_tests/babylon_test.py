import time
from binascii import hexlify

import base58check
import requests

from trezorlib import messages, tezos, ui
from trezorlib.client import TrezorClient
from trezorlib.protobuf import dict_to_proto
from trezorlib.tools import parse_path
from trezorlib.transport import get_transport


def trezor_connect():
    transport = get_transport()
    return TrezorClient(transport, ui=ui.ClickUI())


def inject_operation(op_bytes):
    op_bytes = '"' + hexlify(op_bytes).decode() + '"'
    url = "http://zeronet-node.tzscan.io:80/injection/operation?chain=main"
    http_resp = requests.post(url, data=str(op_bytes))
    print(http_resp.content)
    print(http_resp.status_code)


def get_counter(addr):
    url = "http://zeronet-node.tzscan.io:80/chains/main/blocks/head/context/contracts/{}/counter".format(
        addr
    )
    http_resp = requests.get(url)
    counter = http_resp.content.decode()
    counter = counter.strip("\n").strip('"')
    counter = int(counter) + 1
    return counter


client = trezor_connect()

path = parse_path("m/44'/1729'/10'")

# get branch
http_resp = requests.get(
    "http://zeronet-node.tzscan.io:80/chains/main/blocks/head/hash"
)
branch = http_resp.content.decode()
branch = branch.strip("\n").strip('"')
# print(branch)

# strip the prefix and the 4 checksum bytes

branch_decoded = base58check.b58decode(branch)
branch_decoded = branch_decoded.hex()[4:68]
# print(branch_decoded)

# get address from trezor and decode it
addr = tezos.get_address(client, path)
addr_decoded = base58check.b58decode(addr)
addr_decoded = addr_decoded[3 : len(addr_decoded) - 4].hex()
addr_decoded = "00" + addr_decoded
# print(addr_decoded)

pk = tezos.get_public_key(client, path)
pk_decoded = base58check.b58decode(pk)
pk_decoded = pk_decoded[4 : len(pk_decoded) - 4].hex()
pk_decoded = "00" + pk_decoded

# print("Transaction: ")

# resp = tezos.sign_tx(
#     client,
#     path,
#     dict_to_proto(
#         messages.TezosSignTx,
#         {
#             "branch": branch_decoded,
#             "transaction": {
#                 "source": addr_decoded,
#                 "fee": 20000,
#                 "counter": get_counter(addr),
#                 "gas_limit": 20000,
#                 "storage_limit": 20000,
#                 "amount": 200000,
#                 "destination": {
#                     "tag": 0,
#                     "hash": "0004115bce5af2f977acbb900f449c14c53e1d89cf",
#                 },
#             },
#         },
#     ),
# )

# # inject_operation(resp.sig_op_contents)
# time.sleep(2)
# print("Origination")
# # time.sleep(40)

# resp = tezos.sign_tx(
#     client,
#     path,
#     dict_to_proto(
#         messages.TezosSignTx,
#         {
#             "branch": branch_decoded,
#             "origination": {
#                 "source": addr_decoded,
#                 "fee": 20000,
#                 "counter": get_counter(addr),
#                 "gas_limit": 20000,
#                 "storage_limit": 10000,
#                 "balance": 100000,
#                 "script": "0000001c02000000170500036805010368050202000000080316053d036d03420000000a010000000568656c6c6f",
#             },
#         },
#     ),
# )

# #i nject_operation(resp.sig_op_contents)

# time.sleep(2)
# print("Delegation: ")
# # time.sleep(40)

# resp = tezos.sign_tx(
#     client,
#     path,
#     dict_to_proto(
#         messages.TezosSignTx,
#         {
#             "branch": branch_decoded,
#             "delegation": {
#                 "source": addr_decoded,
#                 "fee": 20000,
#                 "counter": get_counter(addr),
#                 "gas_limit": 20000,
#                 "storage_limit": 20000,
#                 "delegate": "005f450441f41ee11eee78a31d1e1e55627c783bd6",
#             },
#         },
#     ),
# )


# # inject_operation(resp.sig_op_contents)

# time.sleep(2)
# resp = tezos.sign_tx(
#     client,
#     path,
#     dict_to_proto(
#         messages.TezosSignTx,
#         {
#             "branch": branch_decoded,
#             "reveal": {
#                 "source": addr_decoded,
#                 "fee": 20000,
#                 "counter": get_counter(addr),
#                 "gas_limit": 20000,
#                 "storage_limit": 20000,
#                 "public_key": pk_decoded,
#             },
#             "transaction": {
#                 "source": addr_decoded,
#                 "fee": 50000,
#                 "counter": get_counter(addr) + 1,
#                 "gas_limit": 20000,
#                 "storage_limit": 20000,
#                 "amount": 100000,
#                 "destination": {
#                     "tag": 0,
#                     "hash": "00e7670f32038107a59a2b9cfefae36ea21f5aa63c",
#                 },
#             },
#         },
#     ),
# )
# time.sleep(2)
# resp = tezos.sign_tx(
#     client,
#     path,
#     dict_to_proto(
#         messages.TezosSignTx,
#         {
#             "branch": branch_decoded,
#             "transaction": {
#                 "source": addr_decoded,
#                 "fee": 50000,
#                 "counter": get_counter(addr),
#                 "gas_limit": 20000,
#                 "storage_limit": 20000,
#                 "amount": 100000,
#                 "destination": {
#                     "tag": 1,
#                     "hash": "8b83360512c6045c1185f8000de41302e23a220c00",
#                 },
#             },
#         },
#     ),
# )

# inject_operation(resp.sig_op_contents)


# 018b83360512c6045c1185f8000de41302e23a220c00

# resp = tezos.sign_tx(
#     client,
#     path,
#     dict_to_proto(
#         messages.TezosSignTx,
#         {
#             "branch": branch_decoded,
#             "transaction": {
#                 "source": addr_decoded,
#                 "fee": 50000,
#                 "counter": get_counter(addr),
#                 "gas_limit": 20000,
#                 "storage_limit": 200,
#                 "amount": 0,
#                 "destination": {
#                     "tag": 1,
#                     "hash": "8b83360512c6045c1185f8000de41302e23a220c00",
#                 },
#                 "manager_smart_contract_params": {
#                     "transfer": {
#                         "amount": 2000000,
#                         "destination": "005f450441f41ee11eee78a31d1e1e55627c783bd6",
#                     }
#                 },
#             },
#         },
#     ),
# )

resp = tezos.sign_tx(
    client,
    path,
    dict_to_proto(
        messages.TezosSignTx,
        {
            "branch": "38f027151adbf750cf05f5e7259fd7e1d8122a7f76be5204c0db5eb93757c3e4",
            "transaction": {
                "source": "005f450441f41ee11eee78a31d1e1e55627c783bd6",
                "fee": 2857,
                "counter": 196,
                "gas_limit": 25822,
                "storage_limit": 0,
                "amount": 0,
                "destination": {
                    "tag": 1,
                    "hash": "8b83360512c6045c1185f8000de41302e23a220c00",
                },
                "manager_smart_contract_params": {
                    "cancel_delegate": True,
                },
            },
        },
    ),
)

# inject_operation(resp.sig_op_contents)
