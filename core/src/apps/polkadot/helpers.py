if False:
    from trezor.utils import Writer

from micropython import const

from trezor import wire
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


def scale_int_encode(w: Writer, value, compact=True):
    # Simple Concatenated Aggregate Little-Endian(SCALE)
    if value < 0:
        wire.DataError('Only positive values allowed into SCALE encoding')

    # compact encoding
    if compact:
        # single byte mode - 0b00
        if value < 0x3F:
            w.append(value << 2)
        # two-byte mode - 0b01
        elif value < 0x3FFF:
            value = value << 2 | 0x01
            w.append(value & 0xFF)
            w.append((value >> 8) & 0xFF)
        # four-byte mode - 0b10
        elif value < 0x3FFFFFFF:
            value = value << 2 | 0x02
            w.append(value & 0xFF)
            w.append((value >> 8) & 0xFF)
            w.append((value >> 16) & 0xFF)
            w.append((value >> 24) & 0xFF)
        # Big-integer mode - 0b11
        else:
            print('Big int')
            no_of_bytes = get_byte_count(value)
            w.append(((no_of_bytes - 4) << 2 | 0x03) & 0xFF)
            for i in range(0, no_of_bytes * 8, 8):
                print(i)
                w.append((value >> i) & 0xFF)


def scale_list_encode(w, tx_elements: list):
    scale_int_encode(w, len(tx_elements))
    for e in tx_elements:
        scale_int_encode(w, e)


def scale_encode_address(address):
    return bytes([0xff]) + address


def get_byte_count(val: int):
    if val == 0:
        return 1
    elif val > 0:
        count = 0
        while val != 0:
            val >>= 8
            count += 1
        return count
