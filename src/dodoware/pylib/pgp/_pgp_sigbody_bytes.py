from ._pgp_datasource import PgpDataSource
from ._pgp_sigbody import PgpSigBody

class PgpSigBodyBytes(PgpSigBody):
    """
    This class represents the body of a PGP signature subpacket that
    can be represented as a simple `bytes` obect.
    """

    def __init__(self, bodylen:int, datasource:PgpDataSource):

        super().__init__(bodylen)

        self.data = datasource.get_chunk(bodylen)
