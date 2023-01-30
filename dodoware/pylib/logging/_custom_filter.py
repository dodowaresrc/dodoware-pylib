import logging

class CustomFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    """
    A custom log filter that defines two new log record fields:

        whence:
            Combines the `module`, `funcName`, and `lineno` fields so they can be
            referenced as a single string by a log formatter.

        shortlevel:
            An abbreviated form of the log level name.
    """

    # Map a subset of standard logging level names to a corresponding abbreviated name.
    # For level names not in the map (like `INFO`), the abbreviated name is the same
    # as the standard level name.
    SHORT_LEVEL_NAME_MAP = {"CRITICAL": "CRIT", "WARNING": "WARN"}

    def filter(self, record):
        """
        Set the `whence` and `shortlevel` fields for the input log record.
        """

        record.whence = f"{record.module}.{record.funcName}:{record.lineno}"

        record.shortlevel = self.SHORT_LEVEL_NAME_MAP.get(
            record.levelname, record.levelname
        )

        return True
