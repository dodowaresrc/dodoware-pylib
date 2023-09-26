from typing import List

from ._pgp_enum import PgpSignatureType, PgpPublicKeyType, PgpHashType, PgpSigpacketType
from ._pgp_sigpacket import PgpSigPacket

class PgpSignature:
    """
    A PGP signature.
    """

    def __init__(
        self,
        signature_type:PgpSignatureType,
        public_key_type:PgpPublicKeyType,
        hash_type:PgpHashType,
        hashed_sigpackets:List[PgpSigPacket],
        unhashed_sigpackets:List[PgpSigPacket],
        left16:bytes,
        signature:bytes
    ):

        self.signature_type = signature_type
        self.public_key_type = public_key_type
        self.hash_type = hash_type
        self.hashed_sigpackets = hashed_sigpackets
        self.unhashed_sigpackets = unhashed_sigpackets
        self.left16 = left16
        self.signature = signature

    def get_signed_data(self) -> bytearray:
        """
        Get the signature signed data.
        """

        ####
        # RFC section 5.2.4:
        #
        # A V4 signature hashes the packet body
        # starting from its first field, the version number, through the end
        # of the hashed subpacket data.  Thus, the fields hashed are the
        # signature version, the signature type, the public-key algorithm, the
        # hash algorithm, the hashed subpacket length, and the hashed
        # subpacket body.
        ####

        total_hashed_sigpacket_length = 0
        for sigpacket in self.hashed_sigpackets:
            total_hashed_sigpacket_length += len(sigpacket.sigpacket_header)
            total_hashed_sigpacket_length += len(sigpacket.sigpacket_data)

        signed_data = bytearray()

        signed_data.append(4) # version 4

        signed_data.append(self.signature_type.value.type_id)

        signed_data.append(self.public_key_type.value.type_id)

        signed_data.append(self.hash_type.value.type_id)

        signed_data.append((total_hashed_sigpacket_length >> 8) & 0xFF)

        signed_data.append(total_hashed_sigpacket_length & 0xFF)

        for sigpacket in self.hashed_sigpackets:
            signed_data.extend(sigpacket.sigpacket_header)
            signed_data.extend(sigpacket.sigpacket_data)

        ####
        # RFC section 5.2.4:
        #
        # V4 signatures also hash in a final trailer of six octets: the
        # version of the Signature packet, i.e., 0x04; 0xFF; and a four-octet,
        # big-endian number that is the length of the hashed data from the
        # Signature packet (note that this number does not include these final
        # six octets).
        ####

        # Despite the above commentary, in particular the final parenthetical
        # phrase, it appears that the final hashed four-octet length should be
        # incremented by 6 to account for this trailer.  That is how it is done
        # in the GnuPG implementation:
        #
        # https://github.com/gpg/gnupg/blob/master/g10/sig-check.c
        #

        total_hashed_sigpacket_length += 6
        signed_data.append(0x04) # version 4
        signed_data.append(0xFF)
        signed_data.append((total_hashed_sigpacket_length >> 24) & 0xFF)
        signed_data.append((total_hashed_sigpacket_length >> 16) & 0xFF)
        signed_data.append((total_hashed_sigpacket_length >> 8) & 0xFF)
        signed_data.append(total_hashed_sigpacket_length & 0xFF)

        return signed_data

    def get_sigpackets(self, sigpacket_type:PgpSigpacketType, hashed:bool=None) -> List[PgpSigPacket]:
        """
        Get a list of signature subpackets by type.

        Args:
            sigpacket_type (PgpSigpacketType):
                The signature subpacket type.
            hashed (bool):
                If `True`, get hashed sigpackets.  If `False`, get unhashed sigpackets.
                If `None`, get both hashed and unhashed sigppackets.

        Returns:
            List[PgpSigPacket]:
                A list of matching PGP signature subpackets.
        """

        matching_sigpackets = []

        if hashed in (True, None):
            for sigpacket in self.hashed_sigpackets:
                if sigpacket.sigpacket_type == sigpacket_type:
                    matching_sigpackets.append(sigpacket)

        if hashed in (False, None):
            for sigpacket in self.unhashed_sigpackets:
                if sigpacket.sigpacket_type == sigpacket_type:
                    matching_sigpackets.append(sigpacket)

        return matching_sigpackets

    def get_sigpacket(self, sigpacket_type:PgpSigpacketType, must_exist:bool=False, hashed:bool=False) -> PgpSigPacket:
        """
        Get a single signature subpacket by type.  Only one packet of the input type may exist.

        Args:
            sigpacket_type (PgpPacketType):
                The signature subpacket type.
            must_exist (bool):
                If set, a matching sigpacket must exist.
            hashed (bool):
                If `True`, get hashed sigpackets.  If `False`, get unhashed sigpackets.
                If `None`, get both hashed and unhashed sigppackets.

        Returns:
            PgpPacket:
                The matching PGP packets, or `None` if not found.
        """

        sigpacket_list = self.get_sigpackets(sigpacket_type)

        if len(sigpacket_list) > 1:
            raise RuntimeError(f"multiple sigpackets found for sigpacket_type: {sigpacket_list}")

        if sigpacket_list:
            return sigpacket_list[0]

        if must_exist:
            raise RuntimeError(f"packet not found for packet_type: {sigpacket_type}")

        return None
