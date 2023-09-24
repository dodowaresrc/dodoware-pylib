from ._pgp_body import PgpBody
from ._pgp_header import PgpHeader

class PgpPacket:
    """
    This class represents a PGP packet.
    """

    def __init__(self, header:PgpHeader, body:PgpBody):

        self.header = header
        self.body = body
