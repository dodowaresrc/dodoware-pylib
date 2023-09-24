from enum import Enum
from typing import Type

from ._pgp_body import PgpBody
from ._pgp_body_signature import PgpBodySignature
from ._pgp_body_public_key import PgpBodyPublicKey
from ._pgp_body_user_id import PgpBodyUserId

class PgpPacketTag:
    """
    A PGP packet tag.  See RFC section 4.3.
    """

    def __init__(self, tag_id:int, tag_name:str, body_class:Type[PgpBody]):

        self.tag_id = tag_id
        self.tag_name = tag_name
        self.body_class = body_class

class PgpEnumPacketTag(Enum):
    """
    An enumeration of PGP packet tags.  See RFC section 4.3.  This list is incomplete.
    """

    SIGNATURE  = PgpPacketTag(2,  "Signature Packet",  PgpBodySignature)
    PUBLIC_KEY = PgpPacketTag(6,  "Public-Key Packet", PgpBodyPublicKey)
    USER_ID    = PgpPacketTag(13, "User ID Packet",    PgpBodyUserId)
