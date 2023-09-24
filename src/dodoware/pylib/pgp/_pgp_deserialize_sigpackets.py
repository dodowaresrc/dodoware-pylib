from typing import List

from ._pgp_datasource import PgpDataSource
from ._pgp_sigpacket import PgpSigPacket
from ._pgp_sigheader import PgpSigHeader

def pgp_deserialize_sigpackets(datasource:PgpDataSource) -> List[PgpSigPacket]:
    """
    Deserialize signature subpackets from a datasource.
    """

    sigpacket_list = []

    while datasource.avail > 0:

        header = PgpSigHeader(datasource)

        bodylen = header.sigpacket_length - 1 # minus 1 for the type octet

        body_class = header.sigpacket_type.value.sigbody_class

        body = body_class(bodylen, datasource)

        sigpacket = PgpSigPacket(header, body)

        sigpacket_list.append(sigpacket)

    return sigpacket_list
