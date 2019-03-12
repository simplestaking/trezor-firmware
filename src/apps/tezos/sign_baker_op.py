from trezor import wire, loop
from trezor.crypto import hashlib
from trezor.crypto.curve import ed25519
from trezor.messages.TezosSignedBakerOp import TezosSignedBakerOp

from apps.common import paths
from apps.tezos import helpers, layout, writers
from apps.tezos.writers import (
    write_bool,
    write_bytes,
    write_uint8,
    write_uint16,
    write_uint32,
    write_uint64,
)


async def sign_baker_op(ctx, msg, keychain):
    paths.validate_path(ctx, helpers.validate_full_path, path=msg.address_n)
    node = keychain.derive(msg.address_n, helpers.TEZOS_CURVE)

    if helpers.check_baking_confirmed():
        # Accept endorsements and block headers only, otherwise lock the device
        if _check_operation_watermark(msg.magic_byte):
            w = bytearray()
            _get_operation_bytes(w, msg)
            sig_prefixed = await _sign(ctx, bytes(w), node, msg)
        else:
            await helpers.prompt_pin()
            helpers.set_staking_state(False)
            raise wire.DataError("Invalid operation")

        return TezosSignedBakerOp(signature=sig_prefixed)
    else:
        raise wire.DataError("Invalid operation")


def _get_operation_bytes(w: bytearray, msg):
    write_bytes(w, msg.magic_byte)
    write_bytes(w, msg.chain_id)

    if msg.endorsement is not None:
        write_bytes(w, msg.endorsement.branch)
        write_uint8(w, msg.endorsement.tag)
        write_uint32(w, msg.endorsement.level)
    elif msg.block_header is not None:
        write_uint32(w, msg.block_header.level)
        write_uint8(w, msg.block_header.proto)
        write_bytes(w, msg.block_header.predecessor)
        write_uint64(w, msg.block_header.timestamp)
        write_uint8(w, msg.block_header.validation_pass)
        write_bytes(w, msg.block_header.operations_hash)
        write_uint32(w, msg.block_header.bytes_in_field_fitness)
        write_uint32(w, msg.block_header.bytes_in_next_field)
        write_bytes(w, msg.block_header.fitness)
        write_bytes(w, msg.block_header.context)
        write_uint16(w, msg.block_header.priority)
        write_bytes(w, msg.block_header.proof_of_work_nonce)
        write_bool(w, msg.block_header.presence_of_field_seed_nonce_hash)
        if msg.block_header.seed_nonce_hash:
            write_bytes(w, msg.block_header.seed_nonce_hash)


def _check_operation_watermark(watermark):
    # payload must be endorsement - 0x02 or block - 0x01
    return watermark[0] in [1, 2]


async def _sign(ctx, w, node, msg):
    wm_opbytes_hash = hashlib.blake2b(w, outlen=32).digest()
    signature = ed25519.sign(node.private_key(), wm_opbytes_hash)
    sig_prefixed = helpers.base58_encode_check(
        signature, prefix=helpers.TEZOS_SIGNATURE_PREFIX
    )

    if msg.endorsement is not None:
        await layout.show_endorsement_operation(msg)
    elif msg.block_header is not None:
        await layout.show_baking_operation(msg)

    await ctx.wait(loop.sleep(4 * 1000 * 1000))

    return sig_prefixed
