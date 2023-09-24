from ._pgp_sigheader import PgpSigHeader
from ._pgp_sigbody import PgpSigBody

class PgpSigPacket:
    """
    This class represents a PGP signature subpacket.
    """

    def __init__(self, header:PgpSigHeader, body:PgpSigBody):

        self.header = header
        self.body = body
