from micropython import const

from trezor.crypto import base58

from apps.common import HARDENED
from apps.common.writers import write_uint8


def base58_encode_check(payload, prefix=None):
    result = payload
    if prefix is not None:
        result = bytes(prefix) + payload
    return base58.encode_check(result)


def validate_full_path(path: list) -> bool:
    # TODO
    pass