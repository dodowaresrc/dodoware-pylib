from typing import Any

from ._pgp_enum import PgpSigpacketType

class PgpSigPacket:
    """
    This class represents a PGP signature subpacket.
    """

    def __init__(self,
        sigpacket_header:bytes,
        sigpacket_length:int,
        sigpacket_type:PgpSigpacketType,
        sigpacket_data:bytes,
        sigpacket_value:Any
    ):

        self.sigpacket_header = sigpacket_header
        self.sigpacket_length = sigpacket_length
        self.sigpacket_type = sigpacket_type
        self.sigpacket_data = sigpacket_data
        self.sigpacket_value = sigpacket_value
