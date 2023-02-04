import logging

class StreamSettings:
    """
    This class defines how data is read from a stream and what to do with it.
    """

    def __init__(self,
        outfile:str=None,
        overwrite:bool=False,
        logger:logging.Logger=None,
        log_level:int=None,
        log_prefix:str=None,
        max_stash_kb:int=0,
        read_bytes:int=0
    ):
        """
        Args:
            outfile (str):
                If set, data read from the stream will be written to this file.
            overwrite (bool):
                Flag to allow overwriting an existing output file.
            logger (logging.Logger):
                If set, lines of text read from the stream will be logged to
                this logger.  Any trailing whitepace is stripped from text
                before being logged.
            log_level (int):
                Log level for logged messages.  Ignored unless `logger` is set.
                Default is `logging.DEBUG`.
            log_prefix (str):
                Log message prefix for logged messages.  Ignored unless `logger`
                is set.  Default is no prefix.
            max_stash_kb (int):
                If greater than zero, stash data read from the stream in a byte
                buffer.  This input sets the maximum buffer size in multiples of
                1024 bytes.  The actual maximum buffer size may exceed this input
                value by up to `read_bytes` bytes.  Must be zero or a positive
                integer.  Values greater than `16` should be used with extreme
                caution.  If a stream may produce more than 16k of data, it is
                probably better to write it out to a file instead of caching it
                in memory.
            read_bytes (int):
                Maximum length of data to be read from the stream in a single chunk.
                This is also the maximum line length of text data to be logged to
                the logger (but in bytes, not characters).  If the stream content
                has lines of data exceeding this value, it will be broken up into
                multiple log events.  Default value is `128`.  Must be a positive
                integer.
        """

        self.outfile = outfile
        self.overwrite = overwrite
        self.logger = logger
        self.log_level = log_level or logging.DEBUG
        self.log_prefix = log_prefix or ""
        self.max_stash_kb = max_stash_kb if max_stash_kb > 0 else 0
        self.read_bytes = read_bytes if read_bytes > 0 else 128
        