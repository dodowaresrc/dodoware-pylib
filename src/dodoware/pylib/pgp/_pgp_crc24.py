CRC24_INIT = 0x00B704CE
CRC24_POLY = 0x01864CFB
CRC24_BIT25 = 0x01000000
CRC24_MASK = 0x00FFFFFF

def pgp_crc24(crc_data:bytes) -> int:
    """
    PGP CRC-24 algorithm.  See RFC section 6.1.
    """

    crc24 = CRC24_INIT

    for octet in crc_data:
        crc24 ^= (octet << 16)
        for _ in range(8):
            crc24 <<= 1
            if crc24 & CRC24_BIT25:
                crc24 ^= CRC24_POLY

    return crc24 & CRC24_MASK
