from enum import Enum

HEADER_FORMAT = "-----BEGIN {0}-----"
FOOTER_FORMAT = "-----END {0}-----"

class PgpAscType:
    """
    This class represents a particular type of PGP ASCII-armored data.
    See RFC section 6.2.
    """

    def __init__(self, name:str):
        self.name = name
        self.header = HEADER_FORMAT.format(name)
        self.footer = FOOTER_FORMAT.format(name)

    def __str__(self):
        return self.name

class PgpEnumAscType(Enum):
    """
    An enumeration of PGP ASCII-armor data types.  See RFC section 6.2.
    This list is incomplete.
    """

    PGP_MESSAGE           = PgpAscType("PGP MESSAGE")
    PGP_PUBLIC_KEY_BLOCK  = PgpAscType("PGP PUBLIC KEY BLOCK")
    PGP_PRIVATE_KEY_BLOCK = PgpAscType("PGP PRIVATE KEY BLOCK")
    PGP_SIGNATURE         = PgpAscType("PGP SIGNATURE")
