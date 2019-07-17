import namedtupled
from aeternity import signing, transactions, identifiers, node
from aeternity.hashing import encode, _binary, decode, encode_rlp
from trezorlib import messages, aeternity, ui
from trezorlib.client import TrezorClient
from trezorlib.transport import get_transport
from trezorlib.tools import parse_path
from trezorlib.protobuf import dict_to_proto


def trezor_connect():
    transport = get_transport()
    client = TrezorClient(transport, ui=ui.ClickUI())

    return client


client = trezor_connect()

aeternity_cli = node.NodeClient(node.Config(
    external_url="https://sdk-testnet.aepps.com",
))

path = parse_path("m/44'/457'/0'")

nonce = aeternity_cli.get_next_nonce("ak_UG6VFZuuQ9S3gHYWFB8yEXU4Qi6AxFzggXfgtuPfx7Y1qCaob")

tx_builder = transactions.TxBuilder()
txn = tx_builder.tx_spend("ak_UG6VFZuuQ9S3gHYWFB8yEXU4Qi6AxFzggXfgtuPfx7Y1qCaob",
                          "ak_2RB8SwfJp837CtzpLrYNfBJyRhTxM8RhobjWSX84oDUbTH6dE8",
                          1,
                          "txn with tT",
                          0,  # fee, when 0 it is automatically computed
                          0,  # ttl for the transaction in number of blocks (default 0)
                          nonce)

trans = dict_to_proto(messages.AeternitySignTx, {
    "sender_id": "ak_UG6VFZuuQ9S3gHYWFB8yEXU4Qi6AxFzggXfgtuPfx7Y1qCaob",
    "recipient_id": "ak_2RB8SwfJp837CtzpLrYNfBJyRhTxM8RhobjWSX84oDUbTH6dE8",
    "amount": txn.data.amount,
    "fee": txn.data.fee,
    "ttl": txn.data.ttl,
    "nonce": txn.data.nonce,
    "payload": txn.data.payload,
})

ret = aeternity.sign_tx(client, path, trans)

print(ret.raw_bytes.hex())
print(ret.signature)
print(ret.tx_hash)
print(encode(identifiers.TRANSACTION, ret.raw_encoded_tx))

aeternity_cli.broadcast_transaction(encode(identifiers.TRANSACTION, ret.raw_encoded_tx), ret.tx_hash)

print(f"https://testnet.explorer.aepps.com/#/tx/{ret.tx_hash}")
print(f"now waiting for confirmation (it will take ~9 minutes)...")

# aeternity_cli.wait_for_confirmation(ret.tx_hash)

# print(f"transaction confirmed!")
