import base64
import os
import re
from typing import List

from ._pgp_crc24 import pgp_crc24
from ._pgp_datasource import PgpDataSource
from ._pgp_enum import PgpAscType, PgpPacketType
from ._pgp_enum_lookup import pgp_enum_lookup
from ._pgp_packet import PgpPacket

DATA_REGEX = re.compile("^[A-Za-z0-9/+]+=*$")
CRC_REGEX = re.compile("^=([A-Za-z0-9/+]{4})$")
MAXLEN = 16 * 1024

class PgpAscDearmor:
    """
    This class represents data extracted from PGP ASCII-armored text.
    """

    def __init__(self, text:str):

        (self.header, self.data, self.crc, self.footer) = self._process_text(text)

        datasource = PgpDataSource(self.data)

        self.packet_list = datasource.get_packets()

    def get_packets(self, packet_type:PgpPacketType) -> List[PgpPacket]:
        """
        Get a list of packets by type.

        Args:
            packet_type (PgpPacketType):
                The packet type.

        Returns:
            List[PgpPacket]:
                A list of matching PGP packets.
        """

        return [x for x in self.packet_list if x.packet_type == packet_type]

    def get_packet(self, packet_type:PgpPacketType, must_exist=False) -> PgpPacket:
        """
        Get a packet by type.  Only one packet of the input type may exist.

        Args:
            packet_type (PgpPacketType):
                The packet type.
            must_exist (bool):
                If set, a matching packet must exist.

        Returns:
            PgpPacket:
                The matching PGP packets, or `None` if not found.
        """

        packet_list = self.get_packets(packet_type)

        if len(packet_list) > 1:
            raise RuntimeError(f"multiple packets found for packet_type: {packet_type}")
        
        if packet_list:
            return packet_list[0]
        
        if must_exist:
            raise RuntimeError(f"packet not found for packet_type: {packet_type}")
        
        return None

    @classmethod
    def _process_text(cls, text):

        # split the text into lines
        lines = re.split("\r?\n", text)

        # strip trailing whitespace
        lines = [x.rstrip() for x in lines]

        # remove empty lines
        lines = [x for x in lines if x]

        # must contain at least 4 lines
        if len(lines) < 4:
            raise ValueError("insufficient text input (must contain at least 4 lines)")

        # first line must be the header
        header = pgp_enum_lookup(PgpAscType, header=lines[0])
        if not header:
            raise ValueError("invalid text input (first line must be the BEGIN header)")

        # last line must be the footer
        footer = pgp_enum_lookup(PgpAscType, footer=lines[-1])
        if not footer:
            raise ValueError("invalid text input (last line must be the END footer)")

        # header and footer must match
        if header !=footer:
            raise ValueError(f"mismatch: header={header} footer={footer}")

        # next-to-last-line must be the CRC
        m = CRC_REGEX.match(lines[-2])
        if not m:
            raise ValueError("invalid text input (next-to-last line must be the CRC)")
        crc_data = base64.b64decode(m.group(1))
        crc = (crc_data[0] << 16) + (crc_data[1] << 8) + crc_data[2]

        # everything else is data
        data = base64.b64decode("".join(lines[1:-2]))

        # check crc
        actual_crc = pgp_crc24(data)
        if actual_crc != crc:
            raise RuntimeError(f"crc mismatch: actual=0x{actual_crc:08x} expect=0x{crc:08x}")

        return (header, data, crc, footer)

    @classmethod
    def from_file(cls, file, maxlen=MAXLEN):
        """
        Dearmor a file.
        """

        if not os.path.isfile(file):
            raise FileNotFoundError(f"file not found: {file}")

        if maxlen:
            length = os.path.getsize(file)
            if length > maxlen:
                raise ValueError(f"file too large: file={file} length={length} maxlen={maxlen}")

        with open(file, encoding="UTF-8") as f:
            return PgpAscDearmor(f.read())
