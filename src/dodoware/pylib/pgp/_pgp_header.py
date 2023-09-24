
from ._pgp_enum_lookup import pgp_enum_lookup
from ._pgp_enum_packet_tag import PgpEnumPacketTag

class PgpHeader:
    """
    This class represents a PGP packet header.  See RFC section 4.2.
    """

    def __init__(self, datasource):

        # Get the first octet.
        octet0 = datasource.get_octet()

        # Bit 7 must be set.
        if not (octet0 & 0x80):
            raise ValueError(f"invalid octet0=0x{octet0:02x} (bit 7 must be set)")

        # Bit 6 is set for new-style, unset for old-style.
        self.is_newstyle = bool(octet0 & 0x40)

        # Get the packet tag ID.
        if self.is_newstyle:
            # For newstyle, the packet tag is stored in bits 5-0.
            packet_tag = octet0 & 0x3F
        else:
            # For oldstyle, the packet tag is stored in bits 5-2.
            packet_tag = (octet0 & 0x3F) >> 2

        # Get the packet tag enum value.
        self.packet_tag = pgp_enum_lookup(PgpEnumPacketTag, must_exist=True, tag_id=packet_tag)

        # Packet length is encoded differenty for new-style vs. old-style.
        if self.is_newstyle:
            self.packet_length = self._get_newstyle_length(datasource)
        else:
            self.packet_length = self._get_oldstyle_length(octet0, datasource)

    def _get_newstyle_length(self, datasource):
        """
        Get the packet length for a new-style packet.  See RFC section 4.2.2.
        """

        octet1 = datasource.get_octet()

        if octet1 < 0xC0:
            return octet1

        if octet1 < 0xE0:
            octet2 = datasource.get_octet()
            return ((octet1 - 0xC0) << 8) + octet2 + 0xC0

        if octet1 == 0xFF:
            return datasource.get_int(4)

        raise RuntimeError("invalid octet1: 0x{octet1:02x} (partial body lengths not supported)")

    def _get_oldstyle_length(self, octet1, datasource):
        """
        Get the packet length for an old-style packet.  See RFC section 4.2.1.
        """

        length_type = octet1 & 0x03

        if length_type == 0:
            return datasource.get_octet()
        elif length_type == 1:
            return datasource.get_int(2)
        elif length_type == 3:
            return datasource.get_int(4)

        raise RuntimeError(f"invalid length_type: {length_type} (indeterminate body lengths not supported)")
