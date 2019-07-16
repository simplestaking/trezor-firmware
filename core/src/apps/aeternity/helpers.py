from micropython import const

from trezor.crypto import base58

from apps.common import HARDENED
from apps.common.writers import write_uint8

AETERNITY_ACCOUNT_PREFIX = "ak_"
AETERNITY_ACCOUNT_PREFIX_TEST = "tt_"
AETERNITY_TRANSACTION_SIGNATURE_PREFIX = "sg_"
AETERNITY_TRANSACTION_PREFIX = "tx_"


def base58_encode_check_prepend(payload, prefix=None):
    result = base58.encode_check(payload)
    if prefix is not None:
        return prefix + result
    return result


def base58_decode_check_prepend(payload, prefix=None):
    if prefix is not None:
        payload = payload[3:]
    result = base58.decode_check(payload)

    return result
