from ._pgp_datasource import PgpDataSource
from ._pgp_enum_public_key_type import PgpEnumPublicKeyType
from ._pgp_body import PgpBody
from ._pgp_enum_lookup import pgp_enum_lookup

class PgpBodyPublicKey(PgpBody):
    """
    This class represents the body of a PGP public key packet.
    See RFC section 5.5.2. Only V4 RSA key packets are supported.
    """

    def __init__(self, bodylen:int, datasource:PgpDataSource):

        super().__init__(bodylen)

        # A one-octet version number.
        version = datasource.get_octet()

        # Only V4 is supported.
        if version != 4:
            raise RuntimeError(f"invalid public key version: {version}")

        # A four-octet number denoting the time that the key was created.
        self.creation_time = datasource.get_int(4)

        # A one-octet number denoting the public-key algorithm of this key.
        public_key_type_id = datasource.get_octet()
        self.public_key_type = pgp_enum_lookup(PgpEnumPublicKeyType, must_exist=True, type_id=public_key_type_id)

        # Only RSA keys are suppported.
        if not self.public_key_type.value.is_rsa:
            raise RuntimeError("invalid public key type: {self.public_key_type}")

        # Algorithm-Specific Fields for RSA public keys.
        self.rsa_modulus = datasource.get_mpi()
        self.rsa_exponent = datasource.get_mpi()
