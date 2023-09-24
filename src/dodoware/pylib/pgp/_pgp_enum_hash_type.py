from enum import Enum

class PgpHashType:
    """
    This class represents a PGP hash algorithm type.  See RFC section 9.4.
    """
    def __init__(self, type_id, type_name):
        self.type_id = type_id
        self.type_name = type_name

class PgpEnumHashType(Enum):
    """
    An enumeration of PGP hash algorithm types.  See RFC section 9.4.
    This list is incomplete.
    """

    MD5    = PgpHashType(1, "MD5")
    SHA256 = PgpHashType(8, "SHA256")
    SHA384 = PgpHashType(9, "SHA384")
    SHA512 = PgpHashType(10, "SHA512")
    SHA224 = PgpHashType(11, "SHA224")
