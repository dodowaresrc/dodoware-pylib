import logging

from ._get_ex_messages import get_ex_messages

def log_ex_messages(
    logger:logging.Logger,
    ex:BaseException,
    level:int=None,
    traceback:bool=False,
    tb_reverse:bool=False,
    tb_indent:bool=False,
    no_chain:bool=False,
) -> None:

    """
    Log a list of messages for an exception chain.

    Args:
        logger:Logger
            The logger.
        level:int
            The log level for logged messages.  Default is `logging.ERROR`.
        ex:BaseException
            Any exception which may (or may not) begin an exception chain.
        traceback:bool
            If set, include traceback messages for each exception.
        tb_reverse:bool
            If set, reverse the order of traceback messages for each exception.
        tb_indent:bool
            If set, indent traceback messages (ignored unless `traceback` is set).
        no_chain:bool
            If set, do not get messages for chained exceptions.

    Returns:
        List[str]:
            A list of exception messages.
    """

    if level is None:
        level = logging.ERROR

    message_list = get_ex_messages(
        ex,
        traceback=traceback,
        tb_reverse=tb_reverse,
        tb_indent=tb_indent,
        no_chain=no_chain,
    )

    for message in message_list:
        logger.log(level=level, msg=message)
