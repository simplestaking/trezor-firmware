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


class TxSigner:
    """
    TxSigner is used to sign transactions
    """

    def __init__(self, network_id):
        if network_id is None:
            raise ValueError("Network ID must be set to sign transactions")
        self.network_id = network_id

    def encode_signed_transaction(self, transaction, signature):
        """prepare a signed transaction message"""
        tag = bytes([identifiers.OBJECT_TAG_SIGNED_TRANSACTION])
        vsn = bytes([identifiers.VSN])
        encoded_signed_tx = encode_rlp(identifiers.TRANSACTION, [tag, vsn, [signature], transaction])
        encoded_signature = encode(identifiers.SIGNATURE, signature)
        return encoded_signed_tx, encoded_signature

    def sign_encode_transaction(self, tx, signature, metadata: dict = None):
        """
        Sign, encode and compute the hash of a transaction
        :param tx: the TxObject to be signed
        :param metadata: additional data to include in the output of the signed transaction object
        :return: encoded_signed_tx, encoded_signature, tx_hash
        """
        # decode the transaction if not in native mode
        transaction = transactions._tx_native(op=transactions.UNPACK_TX, tx=tx.tx if hasattr(tx, "tx") else tx)
        # get the transaction as byte list
        tx_raw = decode(transaction.tx)

        # sign the transaction
        # signature = self.account.sign(_binary(self.network_id) + tx_raw)
        # encode the transaction
        encoded_signed_tx, _ = self.encode_signed_transaction(tx_raw, decode(signature))
        # compute the hash
        tx_hash = transactions.TxBuilder.compute_tx_hash(encoded_signed_tx)
        # return the object
        tx = dict(
            data=transaction.data,
            metadata=metadata,
            tx=encoded_signed_tx,
            hash=tx_hash,
            signature=signature,
            network_id=self.network_id,
        )
        return namedtupled.map(tx, _nt_name="TxObject")


# def encode_signed_transaction(transaction, signed_msg, sender_blob, metadata: dict = None):
#     tx_signer = transactions.TxSigner(
#         sender_blob,
#         identifiers.NETWORK_ID_TESTNET  # ae_uat
#     )
#     encoded_signed_tx, _ = tx_signer.encode_signed_transaction(signed_msg.raw_bytes, signed_msg.signature)
#     tx_hash = transactions.TxBuilder.compute_tx_hash(encoded_signed_tx)
#     tx_dict = dict(
#         data=transaction.data,
#         metadata=metadata,
#         tx=encoded_signed_tx,
#         hash=tx_hash,
#         signature=signed_msg.signature,
#         network_id=tx_signer.network_id,
#     )
#     return namedtupled.map(tx_dict, _nt_name="TxObject")

client = trezor_connect()
path = parse_path("m/44'/457'/0'")

# generate a new account
recipient_account = signing.Account.from_keystore("Bob.json", "mypassword")
# save the account in an encrypted format
sender_account = signing.Account.from_keystore("Alice.json", "mypassword")
# print the account address
# print("Sender account address: ", sender_account.get_address())

nonce = 1

tx_builder = transactions.TxBuilder()
txn = tx_builder.tx_spend(aeternity.get_address(client, path, show_display=True),
                          recipient_account.get_address(),
                          1000000000000000000,
                          "test tx",
                          0,  # fee, when 0 it is automatically computed
                          0,  # ttl for the transaction in number of blocks (default 0)
                          nonce)

trans = dict_to_proto(messages.AeternitySignTx, {
    "sender_id": aeternity.get_address(client, path, show_display=True),
    "recipient_id": "ak_Ch5udKfQeCRXKMGA4QxL27hKz8anzyBMKVzqY7RSWSq5Abidj",
    "amount": txn.data.amount,
    "fee": txn.data.fee,
    "ttl": txn.data.ttl,
    "nonce": txn.data.nonce,
    "payload": txn.data.payload,
})

ret = aeternity.sign_tx(client, path, trans)
tx_signer = TxSigner(
    identifiers.NETWORK_ID_TESTNET  # ae_uat
)
tx_signed = tx_signer.sign_encode_transaction(txn, ret.signature)

# # Step 2: sign the transaction
tx_signer2 = transactions.TxSigner(
    sender_account,
    identifiers.NETWORK_ID_TESTNET  # ae_uat
)
tx_signed2 = tx_signer2.sign_encode_transaction(txn)

print(ret.raw_bytes.hex())

print(tx_signed.data)
print(tx_signed2.data)
print(tx_signed.tx)
print(tx_signed2.tx)
print(tx_signed.hash)
print(tx_signed2.hash)
print('----------')
print((decode(txn.tx).hex()))

# print(ret.raw_bytes.hex())

# payload_encoded = encode(identifiers.BYTE_ARRAY, _binary("test tx"))
# payload_decoded = decode(payload_encoded)

# print(bytes(payload_decoded).hex())
# print(bytes('test_tx'.encode('utf-8')))

# aeternity_cli = node.NodeClient(node.Config(
#     external_url="https://sdk-testnet.aepps.com",
# ))
#
# aeternity_cli.broadcast_transaction(tx_signed.tx, tx_signed.hash)
#
# print(f"https://testnet.explorer.aepps.com/#/tx/{tx_signed.hash}")
# print(f"now waiting for confirmation (it will take ~9 minutes)...")
#
# # Step 4: [optional] wait for transaction verification
# # the default will wait 3 blocks after the transaction generation blocks
# # the confirmation blocks number can be changed passing the
# # key_block_confirmation_num
# # parameter to teh node.Config
# aeternity_cli.wait_for_confirmation(tx_signed.hash)
#
# print(f"transaction confirmed!")
