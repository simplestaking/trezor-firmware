from micropython import const

from trezor import wire
from trezor.crypto import hashlib
from trezor.crypto.curve import ed25519
from trezor.messages.LibraSignedTx import LibraSignedTx

from apps.common import seed
from apps.common.writers import write_bytes, write_uint64_be, write_uint8

from apps.libra import CURVE


async def sign_tx(ctx, msg, keychain):

    # TODO: validate path

    node = keychain.derive(msg.address_n, CURVE)

    w = bytearray()

    _get_transaction_bytes(w, msg)

    signature = _sign(w, msg, node)
    public_key = seed.remove_ed25519_prefix(node.public_key())

    return LibraSignedTx(
        signature=signature, sender_public_key=public_key, raw_txn_bytes=w
    )


def _get_transaction_bytes(w: bytearray, msg):
    write_bytes(w, msg.sender_account)
    write_uint64_be(w, msg.sequence_number)
    write_bytes(w, msg.program.code)

    for arg in msg.program.args:
        write_uint8(w, arg.type)
        write_bytes(w, arg.data)
    for module in msg.program.modules:
        write_uint64_be(w, module)

    write_uint64_be(w, msg.max_gas_amount)
    if msg.gas_unit_price:
        write_uint64_be(w, msg.gas_unit_price)
    write_uint64_be(w, msg.expiration_time)


def _sign(w: bytearray, msg, node):
    # In libra, we do not sign the raw transaction bytes, but rather the hash of those bytes
    txn_hashvalue = hashlib.sha3_256(w, keccak=True).digest()

    signature = ed25519.sign(node.private_key(), txn_hashvalue)

    return signature

