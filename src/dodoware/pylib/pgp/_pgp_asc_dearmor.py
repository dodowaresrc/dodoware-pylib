import base64
import os
import re

from ._pgp_crc24 import pgp_crc24
from ._pgp_datasource import PgpDataSource
from ._pgp_deserialize_packets import pgp_deserialize_packets
from ._pgp_enum_asc_type import PgpEnumAscType
from ._pgp_enum_lookup import pgp_enum_lookup

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

        self.packet_list = pgp_deserialize_packets(datasource)

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
        header = pgp_enum_lookup(PgpEnumAscType, header=lines[0])
        if not header:
            raise ValueError("invalid text input (first line must be the BEGIN header)")

        # last line must be the footer
        footer = pgp_enum_lookup(PgpEnumAscType, footer=lines[-1])
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
