from aenum import Enum

ASC_HEADER_FORMAT = "-----BEGIN {0}-----"
ASC_FOOTER_FORMAT = "-----END {0}-----"

class PgpAscType(Enum):
    """
    An enumeration of PGP ASCII-armor data types.  See RFC section 6.2.
    This list is incomplete.
    """

    class _Element:
        def __init__(self, name:str):
            self.name = name
            self.header = ASC_HEADER_FORMAT.format(name)
            self.footer = ASC_FOOTER_FORMAT.format(name)

    PGP_MESSAGE           = _Element("PGP MESSAGE")
    PGP_PUBLIC_KEY_BLOCK  = _Element("PGP PUBLIC KEY BLOCK")
    PGP_PRIVATE_KEY_BLOCK = _Element("PGP PRIVATE KEY BLOCK")
    PGP_SIGNATURE         = _Element("PGP SIGNATURE")

class PgpHashType(Enum):
    """
    An enumeration of PGP hash algorithm types.  See RFC section 9.4.
    This list is incomplete.
    """

    class _Element:
        def __init__(self, type_id, type_name):
            self.type_id = type_id
            self.type_name = type_name

    MD5    = _Element(1, "MD5")
    SHA256 = _Element(8, "SHA256")
    SHA384 = _Element(9, "SHA384")
    SHA512 = _Element(10, "SHA512")
    SHA224 = _Element(11, "SHA224")

class PgpPacketType(Enum):
    """
    An enumeration of PGP packet tags.  See RFC section 4.3.  This list is incomplete.
    """

    class _Element:
        def __init__(self, type_id:int, tag_name:str):
            self.type_id = type_id
            self.tag_name = tag_name

    SIGNATURE  = _Element(2,  "Signature Packet")
    PUBLIC_KEY = _Element(6,  "Public-Key Packet")
    USER_ID    = _Element(13, "User ID Packet")

class PgpPublicKeyType(Enum):
    """
    An enumeration of PGP public key types.  See RFC section 9.1.  This list is incomplete.
    """

    class _Element:
        def __init__(self, type_id:int, type_name:str, is_rsa:bool=False):
            self.type_id = type_id
            self.type_name = type_name
            self.is_rsa = is_rsa

    RSA_ENCRYPT_OR_SIGN = _Element(1, "RSA (Encrypt or Sign) [HAC]", is_rsa=True)
    RSA_ENCRYPT_ONLY    = _Element(2, "RSA Encrypt-Only [HAC]", is_rsa=True)
    RSA_SIGN_ONLY       = _Element(3, "RSA Sign-Only [HAC]", is_rsa=True)

class PgpSignatureType(Enum):
    """
    An enumeration of PGP signature types.  See RFC section 5.2.1.
    This list is incomplete.
    """

    class _Element:
        def __init__(self, type_id:int, type_name:str):            
            self.type_id = type_id
            self.type_name = type_name

    BINARY_DOCUMENT          = _Element(0x00, "signature of a binary document")
    TEXT_DOCUMENT            = _Element(0x01, "signature of a canonical text document")
    STANDALONE               = _Element(0x02, "standalone signature")
    GENERIC_USERID           = _Element(0x10, "generic certification of a user id and public-key packet")
    PERSONA_USERID           = _Element(0x11, "persona certification of a user id and public-key packet")
    CASUAL_USERID            = _Element(0x12, "casual certification of a user id and public-key packet")
    POSITIVE_USERID          = _Element(0x13, "positive certification of a user id and public-key packet")
    SUBKEY_BINDING           = _Element(0x18, "subkey binding signature")
    PRIMARY_KEY_BINDING      = _Element(0x19, "primary key binding signature")
    DIRECTLY_ON_A_KEY        = _Element(0x1f, "signature directly on a key")
    KEY_REVOCATION           = _Element(0x20, "key revocation signature")
    SUBKEY_REVOCATION        = _Element(0x28, "subkey revocation signature")
    CERTIFICATION_REVOCATION = _Element(0x30, "certification revocation signature")
    TIMESTAMP                = _Element(0x40, "timestamp signature")
    THIRD_PARTY_CONFIRMATION = _Element(0x50, "third-party confirmation signature")

class PgpSigpacketType(Enum):
    """
    An enumeration of PGP signature subpacket types.  See RFC section 5.2.3.1.
    This list is incomplete.
    """

    class _Element:
        def __init__(self, type_id:int, type_name:str, is_datetime=False, is_string=False, is_int=False):
            self.type_id = type_id
            self.type_name = type_name
            self.is_datetime = is_datetime
            self.is_string = is_string
            self.is_int = is_int

    SIGNATURE_CREATION_TIME          = _Element(2, "Signature Creation Time", is_datetime=True)
    SIGNATURE_EXPIRATION_TIME        = _Element(3, "Signature Expiration Time", is_datetime=True)
    EXPORTABLE_CERTIFICATION         = _Element(4, "Exportable Certification")
    TRUST                            = _Element(5, "Trust Signature")
    REGULAR_EXPRESSION               = _Element(6, "Regular Expression")
    REVOCABLE                        = _Element(7, "Revocable")
    KEY_EXPIRATION_TIME              = _Element(9, "Key Expiration Time", is_datetime=True)
    PREFERRED_SYMMETRIC_ALGORITHMS   = _Element(11, "Preferred Symmetric Algorithms")
    REVOCATION_KEY                   = _Element(12, "Revocation Key")
    ISSUER                           = _Element(16, "Issuer")
    NOTATION_DATA                    = _Element(20, "Notation Data")
    PREFERRED_HASH_ALGORITHMS        = _Element(21, "Preferred Hash Algorithms")
    PREFERRED_COMPRESSION_ALGORITHMS = _Element(22, "Preferred Compression Algorithms")
    KEY_SERVER_PREFERENCES           = _Element(23, "Key Server Preferences")
    PREFERRED_KEY_SERVER             = _Element(24, "Preferred Key Server")
    PRIMARY_USER_ID                  = _Element(25, "Primary User ID")
    POLICY_URI                       = _Element(26, "Policy URI")
    KEY_FLAGS                        = _Element(27, "Key Flags")
    SIGNERS_USER_ID                  = _Element(28, "Signer's User ID")
    REASON_FOR_REVOCATION            = _Element(29, "Reason for Revocation")
    FEATURES                         = _Element(30, "Features")
    SIGNATURE_TARGET                 = _Element(31, "Signature Target")
    EMBEDDED_SIGNATURE               = _Element(32, "Embedded Signature")
    ISSUER_FINGERPRINT               = _Element(33, "Issuer Fingerprint")
