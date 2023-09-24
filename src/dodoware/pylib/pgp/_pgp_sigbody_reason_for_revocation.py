from ._pgp_datasource import PgpDataSource
from ._pgp_sigbody import PgpSigBody

class PgpSigBodyReasonForRevocation(PgpSigBody):
    """
    This class represents the body of a PGP "reason for revocation" signature subpacket.
    """

    def __init__(self, bodylen:int, datasource:PgpDataSource):

        super().__init__(bodylen)

        self.revocation_code = datasource.get_octet()

        self.revocation_reason_data = datasource.get_chunk(bodylen - 1)

        self.revocation_reason = str(self.revocation_reason_data, encoding="UTF-8")
