import hashlib

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

from dodoware.pylib.cmd import Command, CommandTool

from ._pgp_asc_dearmor import PgpAscDearmor
from ._pgp_enum import PgpHashType, PgpPacketType
from ._pgp_public_key import PgpPublicKey
from ._pgp_signature import PgpSignature


class DearmorCommand(Command):
    """ Load data from an ASCII-armored file. """

    def __init__(self, tool):

        super().__init__(tool, "dearmor", "load data from an ASCII-armored file")

    def init_syntax(self):

        self.rg.add_argument("--file", required=True, help="the ASCII-armored file")

    def handle_command(self, pr):

        file = pr.file

        self.logger.info("file=%s", file)

        pgp_dearmor = PgpAscDearmor.from_file(file)

        return pgp_dearmor

class VerifyCommand(Command):
    """ Verify a file against a PGP signature. """

    def __init__(self, tool):

        super().__init__(tool, "verify", "verify a file against a PGP signature")

    def init_syntax(self):

        self.rg.add_argument("--keyfile", required=True, help="ASCII-armored PGP public key file")
        self.rg.add_argument("--sigfile", required=True, help="ASCII-armored PGP signature file")
        self.rg.add_argument("--file", required=True, help="the file to verify")

    def handle_command(self, pr):

        file = pr.file
        keyfile = pr.keyfile
        sigfile = pr.sigfile

        self.logger.info("keyfile=%s", keyfile)
        self.logger.info("sigfile=%s", sigfile)
        self.logger.info("file=%s", file)

        # Dearmor the input keyfile and signature file.
        keyfile_dearmor = PgpAscDearmor.from_file(keyfile)
        sigfile_dearmor = PgpAscDearmor.from_file(sigfile)

        # Get the signature from the signature file.
        signature_packet = sigfile_dearmor.get_packet(PgpPacketType.SIGNATURE)
        signature:PgpSignature = signature_packet.packet_value

        # Get the public key from the keyfile.
        public_key_packet = keyfile_dearmor.get_packet(PgpPacketType.PUBLIC_KEY, must_exist=True)
        public_key:PgpPublicKey = public_key_packet.packet_value

        # Get the hasher.
        if signature.hash_type == PgpHashType.SHA512:
            hasher = hashlib.sha512()
            algorithm = hashes.SHA512()
        elif signature.hash_type == PgpHashType.SHA256:
            hasher = hashlib.sha256()
            algorithm = hashes.SHA256()
        else:
            raise RuntimeError(f"unexpected hash type: {signature.hash_type}")

        # Hash the data file.
        with open(file, mode="rb") as f:
            while True:
                chunk = f.read(512)
                if not chunk:
                    break
                hasher.update(chunk)

        # Hash the signed data from the signature.
        signed_data = signature.get_signed_data()
        hasher.update(signed_data)

        # Verify!
        digest = hasher.digest()
        prehash = Prehashed(algorithm)
        public_key.public_key.verify(signature.signature, digest, padding=PKCS1v15(), algorithm=prehash)

class PgpTool(CommandTool):
    """ A simple tool to excercise some PGP functionality. """

    @property
    def description(self):
        return "a very basic and incomplete PGP implementation"

    def get_command_classes(self):
        return (DearmorCommand, VerifyCommand)
