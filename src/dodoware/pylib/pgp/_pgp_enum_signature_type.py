from enum import Enum

class PgpSignatureType:
    """
    A PGP signature type.  See RFC section 5.2.1.
    """

    def __init__(self, type_id:int, type_name:str):
         
         self.type_id = type_id
         self.type_name = type_name

class PgpEnumSignatureType(Enum):
    """
    An enumeration of PGP signature types.  See RFC section 5.2.1.
    This list is incomplete.
    """

    BINARY_DOCUMENT          = PgpSignatureType(0x00, "signature of a binary document")
    TEXT_DOCUMENT            = PgpSignatureType(0x01, "signature of a canonical text document")
    STANDALONE               = PgpSignatureType(0x02, "standalone signature")
    GENERIC_USERID           = PgpSignatureType(0x10, "generic certification of a user id and public-key packet")
    PERSONA_USERID           = PgpSignatureType(0x11, "persona certification of a user id and public-key packet")
    CASUAL_USERID            = PgpSignatureType(0x12, "casual certification of a user id and public-key packet")
    POSITIVE_USERID          = PgpSignatureType(0x13, "positive certification of a user id and public-key packet")
    SUBKEY_BINDING           = PgpSignatureType(0x18, "subkey binding signature")
    PRIMARY_KEY_BINDING      = PgpSignatureType(0x19, "primary key binding signature")
    DIRECTLY_ON_A_KEY        = PgpSignatureType(0x1f, "signature directly on a key")
    KEY_REVOCATION           = PgpSignatureType(0x20, "key revocation signature")
    SUBKEY_REVOCATION        = PgpSignatureType(0x28, "subkey revocation signature")
    CERTIFICATION_REVOCATION = PgpSignatureType(0x30, "certification revocation signature")
    TIMESTAMP                = PgpSignatureType(0x40, "timestamp signature")
    THIRD_PARTY_CONFIRMATION = PgpSignatureType(0x50, "third-party confirmation signature")
