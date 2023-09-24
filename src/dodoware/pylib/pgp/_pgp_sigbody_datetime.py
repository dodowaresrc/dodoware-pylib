from datetime import datetime

from ._pgp_datasource import PgpDataSource
from ._pgp_sigbody import PgpSigBody

class PgpSigBodyDateTime(PgpSigBody):
    """
    This class represents the body of a PGP signature subpacket that
    can be represented as a 4-octet timestamp, converted to a `datetime`.
    """

    def __init__(self, bodylen:int, datasource:PgpDataSource):

        super().__init__(bodylen)

        self.data = datasource.get_int(4)

        self.datetime = datetime.utcfromtimestamp(self.data)
