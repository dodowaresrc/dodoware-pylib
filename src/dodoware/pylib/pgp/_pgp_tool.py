import hashlib
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from dodoware.pylib.cmd import Command, CommandTool
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from ._pgp_asc_dearmor import PgpAscDearmor
from ._pgp_enum_packet_tag import PgpEnumPacketTag


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

        keyfile_dearmor = PgpAscDearmor.from_file(keyfile)
        sigfile_dearmor = PgpAscDearmor.from_file(sigfile)

        signature = sigfile_dearmor.packet_list[0].body.signature

        signed_data = sigfile_dearmor.packet_list[0].body.signed_data


        print("signature=%s" % signature.hex())

        print("signed_data=%s" % signed_data.hex())

        public_key_packet_list = [x for x in keyfile_dearmor.packet_list if x.header.packet_tag == PgpEnumPacketTag.PUBLIC_KEY]

        public_key_packet = public_key_packet_list[0]

        rsa_public_numbers = RSAPublicNumbers(n=public_key_packet.body.rsa_modulus, e=public_key_packet.body.rsa_exponent)

        rsa_public_key = rsa_public_numbers.public_key()

        print("rsa_public_key=%s" % rsa_public_key)

        hasher = hashlib.sha512()
        with open(file, mode="rb") as f:
            while True:
                chunk = f.read(512)
                if not chunk:
                    break
                hasher.update(chunk)

        hasher.update(signed_data)
        hash = hasher.digest()
     

        print("hash=%s" % hash.hex())

        #verify_result = rsa_public_key.verify(signature, signed_data, algorithm=hashes.SHA512(), padding=PKCS1v15())

        #print("verify_result=%s" % verify_result)


        return {
            "keyfile_dearmor": keyfile_dearmor,
            "sigfile_dearmor": sigfile_dearmor,
        }
    
class PgpTool(CommandTool):
    """ A simple tool to excercise some PGP functionality. """

    @property
    def description(self):
        return "a very basic and incomplete PGP implementation"

    def get_command_classes(self):
        return (DearmorCommand, VerifyCommand)
