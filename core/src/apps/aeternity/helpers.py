import math
from micropython import const

from trezor.crypto import base58

from apps.common import HARDENED
from apps.common.writers import write_uint8

AETERNITY_ACCOUNT_PREFIX = "ak_"
AETERNITY_ACCOUNT_PREFIX_TEST = "tt_"
AETERNITY_TRANSACTION_SIGNATURE_PREFIX = "sg_"
AETERNITY_TRANSACTION_PREFIX = "tx_"
AETERNITY_TRANSACTION_HASH_PREFIX = "th_"
AETERNITY_OBJECT_TAG_ACCOUNT = 10
AETERNITY_OBJECT_TAG_SIGNED_TRANSACTION = 11
AETERNITY_OBJECT_TAG_SPEND_TRANSACTION = 12
AETERNITY_VSN = 1


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


def format_amount(val: int) -> str:
    digits = len(str(val))

    if 0 < digits <= 8:
        token_name = " picoAE"
        val = val / pow(10, 6)
    elif 8 < digits <= 11:
        token_name = " nanoAE"
        val /= pow(10, 9)
    elif 11 < digits <= 14:
        token_name = " microAE"
        val /= pow(10, 12)
    elif 14 < digits <= 17:
        token_name = " milliAE"
        val /= pow(10, 15)
    else:
        token_name = " AE"
        val /= pow(10, 18)

    return str(val) + token_name
