# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
        EnumTypeBackupType = Literal[0, 1, 2]
    except ImportError:
        pass


class ResetDevice(p.MessageType):
    MESSAGE_WIRE_TYPE = 14

    def __init__(
        self,
        display_random: bool = None,
        strength: int = None,
        passphrase_protection: bool = None,
        pin_protection: bool = None,
        language: str = None,
        label: str = None,
        u2f_counter: int = None,
        skip_backup: bool = None,
        no_backup: bool = None,
        backup_type: EnumTypeBackupType = None,
    ) -> None:
        self.display_random = display_random
        self.strength = strength
        self.passphrase_protection = passphrase_protection
        self.pin_protection = pin_protection
        self.language = language
        self.label = label
        self.u2f_counter = u2f_counter
        self.skip_backup = skip_backup
        self.no_backup = no_backup
        self.backup_type = backup_type

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('display_random', p.BoolType, 0),
            2: ('strength', p.UVarintType, 0),  # default=256
            3: ('passphrase_protection', p.BoolType, 0),
            4: ('pin_protection', p.BoolType, 0),
            5: ('language', p.UnicodeType, 0),  # default=english
            6: ('label', p.UnicodeType, 0),
            7: ('u2f_counter', p.UVarintType, 0),
            8: ('skip_backup', p.BoolType, 0),
            9: ('no_backup', p.BoolType, 0),
            10: ('backup_type', p.EnumType("BackupType", (0, 1, 2)), 0),  # default=Bip39
        }
