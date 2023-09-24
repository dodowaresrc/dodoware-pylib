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
