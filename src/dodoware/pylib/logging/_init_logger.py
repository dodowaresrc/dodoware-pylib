import logging
from typing import List

from ._get_logger import get_logger


def init_logger(name: str, args: List[str]) -> logging.Logger:
    """
    Call `get_logger()` with settings derived from an input list of strings
    interpreted as command-line arguments.

    Args:
        name (str):
            The logger name, as might be passed to `logging.getLogger()`.
        args (List[str]):
            A list of strings interpreted as a set of command-line arguments:
              * The `-d` argument enables debug logging.
              * The `-w` argument enables wide-mode logging.
              * The `-x` argument enables extra-wide-mode logging.
    Returns:
        logging.Logger:
            A logger configured according to the input values.

    Note:
        Logging flags must be set individually as in `["-d", "-w", "-t"]`
        and not combined as in `["-dwt"]`.
    """

    debug = "-d" in args

    wide = "-w" in args

    xtra = "-x" in args

    return get_logger(name, debug=debug, wide=wide, xtra=xtra)
