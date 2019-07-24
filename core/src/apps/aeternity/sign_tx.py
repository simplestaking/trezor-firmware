from micropython import const

from trezor import wire
from trezor.crypto import hashlib, rlp
from trezor.crypto.curve import ed25519
from trezor.messages.AeternitySignedTx import AeternitySignedTx
from trezor.messages import AeternityNetworkType

from apps.aeternity import CURVE, helpers, layout
from apps.common import paths
from apps.common.writers import write_bytes, write_uint8, write_uint32_be

if False:
    from trezor.utils import Writer


async def sign_tx(ctx, msg, keychain):
    # TODO: validate path

    node = keychain.derive(msg.address_n, CURVE)

    if msg.spend is not None:
        await layout.require_confirm_tx(ctx, msg.recipient_id, msg.amount)
        await layout.require_confirm_fee(ctx, msg.amount, msg.fee)
    elif msg.aens_preclaim is not None:
        pass
    elif msg.aens_claim is not None:
        pass
    elif msg.aens_update is not None:
        pass
    elif msg.aens_transfer is not None:
        pass
    elif msg.aens_revoke is not None:
        pass
    elif msg.contract_create is not None:
        pass
    elif msg.contract_call is not None:
        pass
    elif msg.channel_create is not None:
        pass
    elif msg.channel_deposit is not None:
        pass
    elif msg.channel_withdraw is not None:
        pass
    elif msg.channel_close_mutual is not None:
        pass
    elif msg.channel_close_solo is not None:
        pass
    elif msg.channel_slash is not None:
        pass
    elif msg.channel_settle is not None:
        pass
    elif msg.channel_snapshot is not None:
        pass
    elif msg.channel_force_progress is not None:
        pass
    elif msg.oracle_register is not None:
        pass
    elif msg.oracle_query is not None:
        pass
    elif msg.oracle_response is not None:
        pass
    elif msg.oracle_extend is not None:
        pass

    if msg.network == AeternityNetworkType.MainNet:
        network_id = helpers.AETERNITY_NETWORK_ID_MAINNET.encode('utf-8')
    else:
        network_id = helpers.AETERNITY_NETWORK_ID_TESTNET.encode('utf-8')

    w = encode_transaction(msg)
    signature = ed25519.sign(node.private_key(), network_id + w)
    encoded_signed_tx = rlp.encode(
        [
            bytes([helpers.AETERNITY_OBJECT_TAG_SIGNED_TRANSACTION]),
            bytes([helpers.AETERNITY_VSN]),
            [signature],
            w,
        ]
    )

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
        raw_encoded_tx=encoded_signed_tx,
    )


def encode_transaction(msg):
    if msg.spend is not None:
        payload_bytes = bytearray()
        write_bytes(payload_bytes, bytes(_encode_string(msg.payload)))

        tx_fields = [
            _encode_int(helpers.AETERNITY_OBJECT_TAG_SPEND_TRANSACTION),
            _encode_int(helpers.AETERNITY_VSN),
            _encode_id(
                msg.sender_id, helpers.AETERNITY_TRANSACTION_SIGNATURE_PREFIX
            ),
            _encode_id(
                msg.recipient_id, helpers.AETERNITY_TRANSACTION_SIGNATURE_PREFIX
            ),
            _encode_int(msg.amount),
            _encode_int(msg.fee),
            _encode_int(msg.ttl),
            _encode_int(msg.nonce),
            payload_bytes,
        ]
    elif msg.aens_preclaim is not None:
        tx_fields = [
            _encode_int(helpers.AETERNITY_OBJECT_TAG_NAME_SERVICE_PRECLAIM_TRANSACTION),
            _encode_int(helpers.AETERNITY_VSN),
            _encode_id(msg.aens_preclaim.account_id, helpers.AETERNITY_OBJECT_TAG_NAME_SERVICE_PRECLAIM_TRANSACTION),
            _encode_int(msg.nonce),
            _encode_id(msg.aens_preclaim.commitment_id, )
        ]

    return rlp.encode(tx_fields)


# TODO: implement the _binary() encoding method from aepp-sdk
def _encode_string(str):
    return str.encode('utf-8')


def _encode_int(val: int):
    return write_uint_minimum_be(val)


def _encode_id(id_str, prefix):
    w = write_uint_minimum_be(1)

    helpers.base58_decode_check_prepend(
        id_str, prefix=prefix
    )

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


def write_uint_minimum_be(n: int):
    w = bytearray()
    byte_count = get_byte_count(n)

    for i in range(byte_count * 8 - 8, -1, -8):
        w.append((n >> i) & 0xFF)

    return w
