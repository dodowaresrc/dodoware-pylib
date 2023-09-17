import logging
import sys

from dodoware.pylib.logging._custom_filter import CustomFilter

FORMAT_BASIC = "%(message)s"
FORMAT_WIDE = "%(asctime)s %(shortlevel)-5s | %(message)s"
FORMAT_XTRA = "%(asctime)s %(shortlevel)-5s %(whence)-40s | %(message)s"


def get_logger(
    name: str,
    wide: bool = None,
    xtra: bool = False,
    debug: bool = False,
    quiet: bool = False,
    stdout: bool = False,
) -> logging.Logger:

    """
    Get a `logging.Logger` instance configured in a way that is often useful for simple apps and
    unit tests.  It is intended to be called only once for any logger name.  Subsequent calls
    should return a functional logger but all filters and handlers will be cleared and rebuilt.

    Args:
        name (str):
            The logger name, as might be passed to `logging.getLogger()`.
        wide (bool):
            Enable wide-mode log formatting.
        xtra (bool):
            Enable extra-wide-mode log formatting.
        debug (bool):
            Enable debug logging.
        quiet (bool):
            If set, do not log to either stdout or stderr.  Overrides the `stdout` input.
        stdout (bool):
            If set, log to stdout instead of stderr (ignored if `quiet` is set).

    Returns:
        logging.Logger:
            A logger configured according to the input values.
    """

    logger = logging.getLogger(name)

    level = logging.DEBUG if debug else logging.INFO

    fmt = FORMAT_XTRA if xtra else FORMAT_WIDE if wide else FORMAT_BASIC

    formatter = logging.Formatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")

    logger.setLevel(level)

    logger.filters.clear()

    logger.handlers.clear()

    logger.addFilter(CustomFilter())

    if not quiet:
        handler = logging.StreamHandler(sys.stdout if stdout else sys.stderr)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
