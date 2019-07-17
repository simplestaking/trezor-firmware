from micropython import const

from trezor import wire
from trezor.crypto import hashlib, rlp
from trezor.crypto.curve import ed25519
from trezor.messages.AeternitySignedTx import AeternitySignedTx

from apps.common import paths
from apps.common.writers import write_bytes, write_uint8, write_uint32_be
from apps.aeternity import CURVE, helpers, layout

if False:
    from trezor.utils import Writer


async def sign_tx(ctx, msg, keychain):
    #TODO: validate path

    node = keychain.derive(msg.address_n, CURVE)

    await layout.require_confirm_tx(ctx, msg.recipient_id, msg.amount)
    await layout.require_confirm_fee(
        ctx, msg.amount, msg.fee
    )

    # TODO: send the network id in the message
    network_id = "ae_uat"
    enc_ni = network_id.encode('utf-8')

    w = encode_transaction(msg)
    signature = ed25519.sign(node.private_key(), enc_ni + w)
    # TODO: replace 'magic' constants with named ones (identifiers.py)
    encoded_signed_tx = rlp.encode([bytes([11]), bytes([1]), [signature], w])

    signature_perfixed = helpers.base58_encode_check_prepend(
        signature, prefix=helpers.AETERNITY_TRANSACTION_SIGNATURE_PREFIX
    )

    transaction_hash = hashlib.blake2b(encoded_signed_tx, outlen=32).digest()
    tx_hash_encoded = helpers.base58_encode_check_prepend(
        transaction_hash, helpers.AETERNITY_TRANSACTION_HASH_PREFIX
    )

    return AeternitySignedTx(
        signature=signature_perfixed,
        raw_bytes=w,
        tx_hash=tx_hash_encoded,
        raw_encoded_tx=encoded_signed_tx
    )


def encode_transaction(msg):
    payload_bytes = bytearray()
    write_bytes(payload_bytes, bytes(msg.payload.encode('utf-8')))

    tx_fields = [
        _encode_int(12),
        _encode_int(1),
        _encode_id(helpers.base58_decode_check_prepend(msg.sender_id, prefix=helpers.AETERNITY_TRANSACTION_SIGNATURE_PREFIX)),
        _encode_id(helpers.base58_decode_check_prepend(msg.recipient_id, prefix=helpers.AETERNITY_TRANSACTION_SIGNATURE_PREFIX)),
        _encode_int(msg.amount),
        _encode_int(msg.fee),
        _encode_int(msg.ttl),
        _encode_int(msg.nonce),
        payload_bytes
    ]

    return rlp.encode(tx_fields)


def _encode_int(val: int):
    return write_uint_arbitrary_be(val)


def _encode_id(id_str):
    w = write_uint_arbitrary_be(1)
    write_bytes(w, id_str)
    return w


def get_byte_count(val: int):
    if val < 0:
        return None
    elif val == 0:
        return 1
    elif val > 0:
        count = 0
        while val != 0:
            val >>= 8
            count += 1
        return count


def write_uint_arbitrary_be(n: int):
    w = bytearray()
    byte_count = get_byte_count(n)

    for i in range(byte_count * 8 - 8, -1, -8):
        w.append((n >> i) & 0xFF)

    return w
