from datetime import datetime

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from ._pgp_enum import PgpPublicKeyType

class PgpPublicKey:
    """
    A PGP public key.  Only RSA keys are supported.
    """

    def __init__(self, creation_time:datetime, public_key_type:PgpPublicKeyType, public_key:RSAPublicKey):

        self.creation_time = creation_time
        self.public_key_type = public_key_type
        self.public_key = public_key
