from datetime import datetime
from typing import Any, List

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPublicNumbers

from ._pgp_enum import PgpHashType, PgpPacketType, PgpPublicKeyType, PgpSignatureType, PgpSigpacketType
from ._pgp_enum_lookup import pgp_enum_lookup
from ._pgp_packet import PgpPacket
from ._pgp_public_key import PgpPublicKey
from ._pgp_signature import PgpSignature
from ._pgp_sigpacket import PgpSigPacket

class PgpDataSource:
    """
    A very simple datasource used to deserialize PGP objects.
    Intended only for use with short messages where all packets
    will fit comfortably into memory.  This class is not thread-safe.
    """

    def __init__(self, data:bytes):
        """
        Args:
            data (bytes):
                Data containing PGP objects to deserialize.
        """

        self._data = data
        self._datalen = len(self._data)
        self._index = 0

    @property
    def datalen(self) -> int:
        """
        Get the total length of the input data, in octets.
        """

        return self._datalen

    @property
    def avail(self) -> int:
        """
        Get the number of octets currently available to be deserialized.
        """

        return self._datalen - self._index

    def get_chunk(self, length:int) -> bytes:
        """
        Deserialize a chunk of data.

        Args:
            length (int):
                The chunk length.

        Returns:
            bytes:
                The chunk data.
        """

        if length > self.avail:
            raise RuntimeError(f"insufficent data: length={length} avail={self.avail}")

        chunk = self._data[self._index : self._index + length]

        self._index += length

        return chunk

    def get_octet(self) -> int:
        """
        Deserialize a single octet.

        Returns:
            int:
                An integer containing the value of the deserialized octet.
        """

        return self.get_chunk(1)[0]

    def get_int(self, length:int) -> int:
        """
        Deserialize an integer of known length.  See RFC section 3.1.
        This is similar to `get_chunk` but instead of returning the data
        as a `bytes` it is unpacked into a single `int`.

        Args:
            length (int):
                Integer length in octets.

        Returns:
            int:
                The deserialized integer value.
        """

        chunk = self.get_chunk(length)

        intval = 0

        for octet in chunk:
            intval <<= 8
            intval += octet
        return intval

    def get_mpi_chunk(self):
        """
        Get a multiprecision integer (MPI) value, but as a `bytes` object,
        not unpacked into an `int`.  See RFC section 3.2.
        """

        length = self.get_int(2)

        full_octets = int(length/8)

        extra_bits = length % 8

        if extra_bits == 0:
            return self.get_chunk(full_octets)

        first_octet_as_byte_array = bytearray(self.get_chunk(1))

        first_octet_mask = 0xFF >> (8 - extra_bits)

        first_octet_as_byte_array[0] &= first_octet_mask

        first_octet_as_bytes = bytes(first_octet_as_byte_array)

        return first_octet_as_bytes + self.get_chunk(full_octets)

    def get_mpi(self):
        """
        Get a multiprecision integer (MPI).  See RFC section 3.2.
        """

        chunk = self.get_mpi_chunk()

        intval = 0

        for octet in chunk:
            intval <<= 8
            intval += octet

        return intval

    def get_packets(self) -> List[PgpPacket]:
        """
        Deserialize packets from the datasource.
        """

        packet_list = []

        while self.avail > 0:
            packet = self.get_packet()
            packet_list.append(packet)

        return packet_list

    def _get_packet_length_old(self, packet_length_type:int) -> int:
        """
        Deserialize an oldstyle packet length from the datasource.
        """

        if packet_length_type == 0:
            return self.get_octet()

        elif packet_length_type == 1:
            return self.get_int(2)

        elif packet_length_type == 2:
            return self.get_int(4)

        raise RuntimeError(f"invalid packet_length_type: {packet_length_type}")

    def _get_packet_length_new(self) -> int:
        """
        Deserialize a newstyle packet length from the datasource.
        """

        length_octet_1 = self.get_octet()

        if length_octet_1 < 0xC0:
            return length_octet_1

        elif length_octet_1 < 0xE0:
            length_octet_2 = self.get_octet()
            return ((length_octet_1 - 0xC0) << 8) + length_octet_2 + 0xC0

        elif length_octet_1 == 0xFF:
            return self.get_int(4)

        else:
            raise RuntimeError(f"invalid length_octet_1: 0x{length_octet_1:02x}")

    def get_packet(self) -> PgpPacket:
        """
        Deserialize a single packet from the datasource.
        """

        # Get the first octet.
        octet0 = self.get_octet()

        # Bit 7 must be set.
        if not octet0 & 0x80:
            raise ValueError(f"invalid octet0=0x{octet0:02x} (bit 7 must be set)")

        # Bit 6 is set for new-style, unset for old-style.
        is_newstyle = bool(octet0 & 0x40)

        # Get the packet type ID.
        if is_newstyle:
            # For newstyle, the packet tag is stored in bits 5-0.
            packet_type_id = octet0 & 0x3F
        else:
            # For oldstyle, the packet tag is stored in bits 5-2.
            packet_type_id = (octet0 & 0x3F) >> 2

        # Get the packet type enum value.
        packet_type = pgp_enum_lookup(PgpPacketType, must_exist=True, type_id=packet_type_id)

        # Get the packet length.
        packet_length = self._get_packet_length_new() if is_newstyle else self._get_packet_length_old(octet0 & 0x03)

        # Get the packet data.
        packet_data = self.get_chunk(packet_length)

        # Get the packet value.
        packet_value = self._parse_packet_data(packet_type, packet_data)

        # Return a PgpPacket to the caller.
        return PgpPacket(is_newstyle, packet_length, packet_type, packet_data, packet_value)

    def get_public_key(self) -> RSAPublicKey:
        """
        Deserialize a public key from the datasource.  See RFC section 5.5.2.
        Only V4 RSA keys are supported.
        """

        # A one-octet version number.
        version = self.get_octet()

        # Only V4 is supported.
        if version != 4:
            raise RuntimeError(f"invalid public key version: {version}")

        # A four-octet number denoting the time that the key was created.
        creation_time = self.get_int(4)

        # A one-octet number denoting the public-key algorithm of this key.
        public_key_type_id = self.get_octet()
        public_key_type = pgp_enum_lookup(PgpPublicKeyType, must_exist=True, type_id=public_key_type_id)

        # Only RSA keys are suppported.
        if not public_key_type.value.is_rsa:
            raise RuntimeError("invalid public key type: {self.public_key_type}")

        # Algorithm-Specific Fields for RSA public keys.
        rsa_modulus = self.get_mpi()
        rsa_exponent = self.get_mpi()

        # Convert to an RSA public key.
        public_key = RSAPublicNumbers(e=rsa_exponent, n=rsa_modulus).public_key()

        # Return a PgpPublicKey.
        return PgpPublicKey(creation_time, public_key_type, public_key)

    def get_signature(self):
        """
        Deserialize a PGP signature from the datasource.  See RFC section 5.2.3.
        Only V4 RSA signatures are supported.
        """

        # One-octet version number.  Must be Vd4.
        version = self.get_octet()
        if version != 4:
            raise RuntimeError("invalid signature version: {version}")

        # One-octet signature type.
        signature_type = pgp_enum_lookup(PgpSignatureType, must_exist=True, type_id=self.get_octet())

        # One-octet public-key algorithm.  Must be RSA.
        public_key_type = pgp_enum_lookup(PgpPublicKeyType, must_exist=True, type_id=self.get_octet())

        # One-octet hash algorithm.
        hash_type = pgp_enum_lookup(PgpHashType, must_exist=True, type_id=self.get_octet())

        # Two-octet scalar octet count for following hashed subpacket data.
        hashed_datalen = self.get_int(2)

        # Hashed subpacket data, deserialized to signature subpackets.
        hashed_data = self.get_chunk(hashed_datalen)
        hashed_sigpackets = PgpDataSource(hashed_data).get_sigpackets()

        # Two-octet scalar octet count for the following unhashed subpacket data.
        unhashed_datalen = self.get_int(2)

        # Unhashed subpacket data, deserialized to signature subpackets.
        unhashed_data = self.get_chunk(unhashed_datalen)
        unhashed_sigpackets = PgpDataSource(unhashed_data).get_sigpackets()

        # Two-octet field holding the left 16 bits of the signed hash value.
        left16 = self.get_chunk(2)

        # One or more multiprecision integers comprising the signature.
        # For RSA signatures it is a single MPI containing the signature value.
        signature = self.get_mpi_chunk()

        # Return a PgpSignature.
        return PgpSignature(
            signature_type=signature_type,
            public_key_type=public_key_type,
            hash_type=hash_type,
            hashed_sigpackets=hashed_sigpackets,
            unhashed_sigpackets=unhashed_sigpackets,
            left16=left16,
            signature=signature)
   
    @staticmethod
    def _parse_sigpacket_data(sigpacket_type:PgpSigpacketType, sigpacket_data:bytes) -> Any:
        """
        Helper method to parse sigpacket data.
        """

        if sigpacket_type.value.is_datetime:
            if len(sigpacket_data) != 4:
                raise RuntimeError(f"invalid sigpacket_datalen for datetime conversion: {len(sigpacket_data)}")
            intval = 0
            for octet in sigpacket_data:
                intval <<= 8
                intval += octet
            return datetime.utcfromtimestamp(intval)

        if sigpacket_type.value.is_string:      
            return str(sigpacket_data, "UTF-8")

        if sigpacket_type.value.is_int:
            intval = 0
            for octet in sigpacket_data:
                intval <<= 8
                intval += octet
            return intval

        return None

    @staticmethod
    def _parse_packet_data(packet_type:PgpPacketType, packet_data:bytes) -> Any:

        if packet_type == PgpPacketType.PUBLIC_KEY:
            return PgpDataSource(packet_data).get_public_key()

        if packet_type == PgpPacketType.SIGNATURE:
            return PgpDataSource(packet_data).get_signature()

        if packet_type == PgpPacketType.USER_ID:
            return str(packet_data, encoding="UTF-8")

        return None

    def get_sigpacket(self):
        """
        Deserialize a single signature subpacket from the datasource.
        See RFC section 5.2.3.1.
        """

        sigpacket_header = bytearray()

        length_octet_1 = self.get_octet()
        sigpacket_header.append(length_octet_1)

        if length_octet_1 < 0xC0:
            sigpacket_length = length_octet_1

        elif length_octet_1 < 0xFF:
            length_octet_2 = self.get_octet()
            sigpacket_header.append(length_octet_2)
            sigpacket_length = ((length_octet_1 - 0xC0) << 8) + (length_octet_2) + 0xC0

        else:
            sigpacket_length = 0
            for _ in range(4):
                octet = self.get_octet()
                sigpacket_length <<= 8
                sigpacket_length += octet
                sigpacket_header.append(octet)

        # Subpacket length includes the type octet.
        sigpacket_datalen = sigpacket_length - 1

        # The sigpacket type (1 octet).
        sigpacket_type_id = self.get_octet()
        sigpacket_header.append(sigpacket_type_id)
        sigpacket_type = pgp_enum_lookup(PgpSigpacketType, must_exist=True, type_id=sigpacket_type_id)

        # Followed by the subpacket-specific data.
        # The length includes the type octet.
        sigpacket_data = self.get_chunk(sigpacket_datalen)

        # Parse the sigpacket data.
        sigpacket_value = self._parse_sigpacket_data(sigpacket_type, sigpacket_data)

        # Return the sigpacket.
        return PgpSigPacket(
            sigpacket_header=bytes(sigpacket_header),
            sigpacket_length=sigpacket_length,
            sigpacket_type=sigpacket_type,
            sigpacket_data=sigpacket_data,
            sigpacket_value=sigpacket_value)

    def get_sigpackets(self):
        """
        Deserialize signature subpackets from the datasource.
        """

        sigpacket_list = []

        while self.avail > 0:
            sigpacket = self.get_sigpacket()
            sigpacket_list.append(sigpacket)

        return sigpacket_list
