from ._pgp_datasource import PgpDataSource
from ._pgp_enum_signature_type import PgpEnumSignatureType
from ._pgp_enum_public_key_type import PgpEnumPublicKeyType
from ._pgp_enum_hash_type import PgpEnumHashType
from ._pgp_enum_lookup import pgp_enum_lookup
from ._pgp_deserialize_sigpackets import pgp_deserialize_sigpackets
from ._pgp_body import PgpBody

class PgpBodySignature(PgpBody):
    """
    This class represents the body of a PGP signature packet.  See RFC section 5.2.3.
    Only Version 4 signatures are supported.
    """

    def __init__(self, bodylen:int, datasource:PgpDataSource):

        super().__init__(bodylen)

        first_six_octets = datasource.get_chunk(6)

        version = first_six_octets[0]

        if version != 4:
            raise RuntimeError(f"invalid signature version: {version}")

        signature_type_id = first_six_octets[1]

        self.signature_type = pgp_enum_lookup(PgpEnumSignatureType, must_exist=True, type_id=signature_type_id)

        public_key_type_id = first_six_octets[2]

        self.public_key_type = pgp_enum_lookup(PgpEnumPublicKeyType, must_exist=True, type_id=public_key_type_id)

        hash_type_id = first_six_octets[3]

        self.hash_type = pgp_enum_lookup(PgpEnumHashType, must_exist=True, type_id=hash_type_id)

        hashed_sigpackets_octet_count = (first_six_octets[4] << 8) + first_six_octets[5]

        hashed_sigpackets_data = datasource.get_chunk(hashed_sigpackets_octet_count)

        self.signed_data = first_six_octets + hashed_sigpackets_data

        self.hashed_sigpackets = pgp_deserialize_sigpackets(PgpDataSource(hashed_sigpackets_data))

        unhashed_sigpackets_octet_count = datasource.get_int(2)

        unhashed_sigpackets_data = datasource.get_chunk(unhashed_sigpackets_octet_count)

        self.unhashed_sigpackets = pgp_deserialize_sigpackets(PgpDataSource(unhashed_sigpackets_data))

        self.left16 = datasource.get_chunk(2)

        self.signature = datasource.get_mpi_chunk()
