from typing import List

from ._pgp_datasource import PgpDataSource
from ._pgp_packet import PgpPacket
from ._pgp_header import PgpHeader

def pgp_deserialize_packets(datasource:PgpDataSource) -> List[PgpPacket]:
    """
    Deserialize packets from a datasource.
    """

    packet_list = []

    while datasource.avail > 0:

        header = PgpHeader(datasource)

        bodylen = header.packet_length

        body = header.packet_tag.value.body_class(bodylen, datasource)

        packet = PgpPacket(header, body)

        packet_list.append(packet)

    return packet_list
