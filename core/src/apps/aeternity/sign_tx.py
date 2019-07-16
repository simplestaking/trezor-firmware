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

    w = bytearray()
    network_id = "ae_uat"
    enc_ni = network_id.encode('utf-8')

    encode_transaction(w, msg)
    signature = ed25519.sign(node.private_key(), enc_ni + w)
     # encoded_signed_tx = encode_rlp([msg.tag, msg.vsn, [signature], w])

    signature_perfixed = helpers.base58_encode_check_prepend(
        signature, prefix=helpers.AETERNITY_TRANSACTION_SIGNATURE_PREFIX
    )

    return AeternitySignedTx(
        signature=signature_perfixed, raw_bytes=w
    )


# def encode_rlp(data):
#     if not isinstance(data, list):
#         raise ValueError("data to be encoded to rlp must be a list")
#     payload = rlp.encode(data)
#     return helpers.AETERNITY_TRANSACTION_PREFIX + base64.b64encode(payload)


def encode_transaction(w, msg):
    _encode_int(w, 12)
    _encode_int(w, 1)   # vsn
    _encode_id(w, helpers.base58_decode_check_prepend(msg.sender_id, prefix=helpers.AETERNITY_TRANSACTION_SIGNATURE_PREFIX))
    _encode_id(w, helpers.base58_decode_check_prepend(msg.recipient_id, prefix=helpers.AETERNITY_TRANSACTION_SIGNATURE_PREFIX))
    _encode_int(w, msg.amount)
    _encode_int(w, msg.fee)
    _encode_int(w, msg.ttl)
    _encode_int(w, msg.nonce)
    write_bytes(w, bytes(msg.payload.encode('utf-8')))

    # _int(tag),
    # _int(vsn),
    # _id(kwargs.get("sender_id")),
    # _id(kwargs.get("recipient_id")),
    # _int(kwargs.get("amount")),
    # _int(kwargs.get("fee")),  # index 5
    # _int(kwargs.get("ttl")),
    # _int(kwargs.get("nonce")),
    # _binary(kwargs.get("payload"))


def _encode_int(w, val: int):
    write_uint_arbitrary_be(w, val)


def _encode_id(w, id_str):
    write_uint_arbitrary_be(w, 1)
    write_bytes(w, id_str)


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


def write_uint_arbitrary_be(w: Writer, n: int) -> int:
    byte_count = get_byte_count(n)
    print("Encoded int byte count: {}".format(byte_count))

    for i in range(byte_count * 8 - 8, -1, -8):
        w.append((n >> i) & 0xFF)
        print("Bitwise: ({} >> {}) & 0xFF".format(n, i))

    return byte_count
