import abc

class PgpSigBody(metaclass=abc.ABCMeta):
    """
    Base class for types representing bodies of PGP signatures subpackets.
    """

    def __init__(self, bodylen:int):

        self.bodylen = bodylen
