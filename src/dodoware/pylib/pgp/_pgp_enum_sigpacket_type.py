from enum import Enum
from typing import Type

from ._pgp_sigbody import PgpSigBody
from ._pgp_sigbody_reason_for_revocation import PgpSigBodyReasonForRevocation
from ._pgp_sigbody_bytes import PgpSigBodyBytes
from ._pgp_sigbody_datetime import PgpSigBodyDateTime

class PgpSigpacketType:
    """
    A PGP signature subpacket type.  See RFC section 5.2.3.1.
    """

    def __init__(self, type_id:int, type_name:str, sbc:Type[PgpSigBody]=None):

        self.type_id = type_id
        self.type_name = type_name
        self.sigbody_class = sbc or PgpSigBodyBytes

class PgpEnumSigpacketType(Enum):
    """
    An enumeration of PGP signature subpacket types.  See RFC section 5.2.3.1.
    This list is incomplete.
    """

    SIGNATURE_CREATION_TIME          = PgpSigpacketType(2, "Signature Creation Time", sbc=PgpSigBodyDateTime)
    SIGNATURE_EXPIRATION_TIME        = PgpSigpacketType(3, "Signature Expiration Time", sbc=PgpSigBodyDateTime)
    EXPORTABLE_CERTIFICATION         = PgpSigpacketType(4, "Exportable Certification")
    TRUST                            = PgpSigpacketType(5, "Trust Signature")
    REGULAR_EXPRESSION               = PgpSigpacketType(6, "Regular Expression")
    REVOCABLE                        = PgpSigpacketType(7, "Revocable")
    KEY_EXPIRATION_TIME              = PgpSigpacketType(9, "Key Expiration Time", sbc=PgpSigBodyDateTime)
    PREFERRED_SYMMETRIC_ALGORITHMS   = PgpSigpacketType(11, "Preferred Symmetric Algorithms")
    REVOCATION_KEY                   = PgpSigpacketType(12, "Revocation Key")
    ISSUER                           = PgpSigpacketType(16, "Issuer")
    NOTATION_DATA                    = PgpSigpacketType(20, "Notation Data")
    PREFERRED_HASH_ALGORITHMS        = PgpSigpacketType(21, "Preferred Hash Algorithms")
    PREFERRED_COMPRESSION_ALGORITHMS = PgpSigpacketType(22, "Preferred Compression Algorithms")
    KEY_SERVER_PREFERENCES           = PgpSigpacketType(23, "Key Server Preferences")
    PREFERRED_KEY_SERVER             = PgpSigpacketType(24, "Preferred Key Server")
    PRIMARY_USER_ID                  = PgpSigpacketType(25, "Primary User ID")
    POLICY_URI                       = PgpSigpacketType(26, "Policy URI")
    KEY_FLAGS                        = PgpSigpacketType(27, "Key Flags")
    SIGNERS_USER_ID                  = PgpSigpacketType(28, "Signer's User ID")
    REASON_FOR_REVOCATION            = PgpSigpacketType(29, "Reason for Revocation")
    FEATURES                         = PgpSigpacketType(30, "Features")
    SIGNATURE_TARGET                 = PgpSigpacketType(31, "Signature Target")
    EMBEDDED_SIGNATURE               = PgpSigpacketType(32, "Embedded Signature")
    ISSUER_FINGERPRINT               = PgpSigpacketType(33, "Issuer Fingerprint")
    