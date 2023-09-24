from ._pgp_body import PgpBody
from ._pgp_datasource import PgpDataSource

class PgpBodyUserId(PgpBody):
    """
    This class represents the body of a PGP user ID packet.  See RFC section 5.11.
    """

    def __init__(self, bodylen:int, datasource:PgpDataSource):

        super().__init__(bodylen)

        user_id_data = datasource.get_chunk(bodylen)

        self.user_id = str(user_id_data, encoding="UTF-8")
