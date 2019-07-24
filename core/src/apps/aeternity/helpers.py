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
AETERNITY_COMMITMENT_PREFIX = "cm_"  # base58	Commitment

AETERNITY_OBJECT_TAG_ACCOUNT = const(10)
AETERNITY_OBJECT_TAG_SIGNED_TRANSACTION = const(11)
AETERNITY_OBJECT_TAG_SPEND_TRANSACTION = const(12)
AETERNITY_VSN = const(1)
AETERNITY_NETWORK_ID_MAINNET = "ae_mainnet"
AETERNITY_NETWORK_ID_TESTNET = "ae_uat"
AETERNITY_OBJECT_TAG_ORACLE_REGISTER_TRANSACTION = const(22)
AETERNITY_OBJECT_TAG_ORACLE_QUERY_TRANSACTION = const(23)
AETERNITY_OBJECT_TAG_ORACLE_RESPONSE_TRANSACTION = const(24)
AETERNITY_OBJECT_TAG_ORACLE_EXTEND_TRANSACTION = const(25)
AETERNITY_OBJECT_TAG_NAME_SERVICE_CLAIM_TRANSACTION = const(32)
AETERNITY_OBJECT_TAG_NAME_SERVICE_PRECLAIM_TRANSACTION = const(33)
AETERNITY_OBJECT_TAG_NAME_SERVICE_UPDATE_TRANSACTION = const(34)
AETERNITY_OBJECT_TAG_NAME_SERVICE_REVOKE_TRANSACTION = const(35)
AETERNITY_OBJECT_TAG_NAME_SERVICE_TRANSFER_TRANSACTION = const(36)
AETERNITY_OBJECT_TAG_CONTRACT = const(40)
AETERNITY_OBJECT_TAG_CONTRACT_CALL = const(41)
AETERNITY_OBJECT_TAG_CONTRACT_CREATE_TRANSACTION = const(42)
AETERNITY_OBJECT_TAG_CONTRACT_CALL_TRANSACTION = const(43)
AETERNITY_OBJECT_TAG_CHANNEL_CREATE_TRANSACTION = const(50)
AETERNITY_OBJECT_TAG_CHANNEL_DEPOSIT_TRANSACTION = const(51)
AETERNITY_OBJECT_TAG_CHANNEL_WITHDRAW_TRANSACTION = const(52)
AETERNITY_OBJECT_TAG_CHANNEL_FORCE_PROGRESS_TRANSACTION = const(521)
AETERNITY_OBJECT_TAG_CHANNEL_CLOSE_MUTUAL_TRANSACTION = const(53)
AETERNITY_OBJECT_TAG_CHANNEL_CLOSE_SOLO_TRANSACTION = const(54)
AETERNITY_OBJECT_TAG_CHANNEL_SLASH_TRANSACTION = const(55)
AETERNITY_OBJECT_TAG_CHANNEL_SETTLE_TRANSACTION = const(56)
AETERNITY_OBJECT_TAG_CHANNEL_OFF_CHAIN_TRANSACTION = const(57)


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
