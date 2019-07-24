import namedtupled
from aeternity import identifiers, node, signing, transactions
from aeternity.hashing import _binary, decode, encode, encode_rlp
from trezorlib import aeternity, messages, ui
from trezorlib.client import TrezorClient
from trezorlib.protobuf import dict_to_proto
from trezorlib.tools import parse_path
from trezorlib.transport import get_transport


def trezor_connect():
    transport = get_transport()
    client = TrezorClient(transport, ui=ui.ClickUI())

    return client


client = trezor_connect()

aeternity_cli = node.NodeClient(
    node.Config(external_url="https://sdk-testnet.aepps.com")
)

path = parse_path("m/44'/457'/0'/0'/0'")

nonce = aeternity_cli.get_next_nonce(
    "ak_31USV3rnR2UXfJwLUeezNoYscezfeXg8RYDir7kQUzfCbaShi"
)

# generate transaction object
tx_builder = transactions.TxBuilder()
txn = tx_builder.tx_spend(
    "ak_31USV3rnR2UXfJwLUeezNoYscezfeXg8RYDir7kQUzfCbaShi",
    "ak_27GArnMWZFadMReB8q47Y1UvDFGT2g475bLBu8pv36taYLRWsU",
    1000000000000000,
    "txn with tT",
    0,  # fee, when 0 it is automatically computed
    0,  # ttl for the transaction in number of blocks (default 0)
    nonce,
)

# transaction objet -> protobuf messsage
trans = dict_to_proto(
    messages.AeternitySignTx,
    {
        "network": messages.AeternityNetworkType.TestNet,
        "sender_id": txn.data.sender_id,
        "recipient_id": txn.data.recipient_id,
        "amount": txn.data.amount,
        "fee": txn.data.fee,
        "ttl": txn.data.ttl,
        "nonce": txn.data.nonce,
        "payload": txn.data.payload,
    },
)

# sign with trezor
signed_tx = aeternity.sign_tx(client, path, trans)

print(signed_tx.raw_bytes.hex())
print(signed_tx.signature)
print(signed_tx.tx_hash)
print(encode(identifiers.TRANSACTION, signed_tx.raw_encoded_tx))

# encode(prefix + base64encode) the transaction data with included signature
aeternity_cli.broadcast_transaction(
    encode(identifiers.TRANSACTION, signed_tx.raw_encoded_tx), signed_tx.tx_hash
)

print(f"https://testnet.explorer.aepps.com/#/tx/{signed_tx.tx_hash}")
# print(f"now waiting for confirmation (it will take ~9 minutes)...")

# aeternity_cli.wait_for_confirmation(signed_tx.tx_hash)

print(f"transaction confirmed!")
