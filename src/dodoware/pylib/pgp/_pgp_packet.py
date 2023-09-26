from typing import Any

from ._pgp_enum import PgpPacketType

class PgpPacket:
    """
    This class represents a PGP packet.
    """

    def __init__(self, is_newstyle:bool, packet_length:int, packet_type:PgpPacketType, packet_data:bytes, packet_value:Any):

        self.is_newstyle = is_newstyle
        self.packet_length = packet_length
        self.packet_type = packet_type
        self.packet_data = packet_data
        self.packet_value = packet_value
