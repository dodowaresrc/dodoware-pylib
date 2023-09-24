from ._pgp_datasource import PgpDataSource
from ._pgp_enum_lookup import pgp_enum_lookup
from ._pgp_enum_sigpacket_type import PgpEnumSigpacketType

class PgpSigHeader:
    """
    This class represnets a PGP signature subpacket header.  See RFC section 5.2.3.1.
    """

    def __init__(self, datasource:PgpDataSource):

        octet1 = datasource.get_octet()

        if octet1 < 0xC0:
            self.sigpacket_length = octet1
        elif octet1 < 0xFF:
            octet2 = datasource.get_octet()
            self.sigpacket_length = ((octet1 - 0xC0) << 8) + octet2 + 0xC0
        else:
            self.sigpacket_length = datasource.get_int(4)

        sigpacket_type_id = datasource.get_octet()

        self.sigpacket_type = pgp_enum_lookup(PgpEnumSigpacketType, must_exist=True, type_id = sigpacket_type_id)
