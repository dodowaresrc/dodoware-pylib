from enum import Enum

class PgpPublicKeyType:
    """
    A PGP public key type.  See RFC section 9.1.
    """

    def __init__(self, type_id:int, type_name:str, is_rsa:bool=False):

        self.type_id = type_id
        self.type_name = type_name
        self.is_rsa = is_rsa

class PgpEnumPublicKeyType(Enum):
    """
    An enumeration of PGP public key types.  See RFC section 9.1.  This list is incomplete.
    """

    RSA_ENCRYPT_OR_SIGN = PgpPublicKeyType(1, "RSA (Encrypt or Sign) [HAC]", is_rsa=True)
    RSA_ENCRYPT_ONLY    = PgpPublicKeyType(2, "RSA Encrypt-Only [HAC]", is_rsa=True)
    RSA_SIGN_ONLY       = PgpPublicKeyType(3, "RSA Sign-Only [HAC]", is_rsa=True)
