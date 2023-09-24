import abc

class PgpBody(metaclass=abc.ABCMeta):
    """
    Base class for PGP packet body types.
    """

    def __init__(self, packet_length:int):

        self.packet_length = packet_length
