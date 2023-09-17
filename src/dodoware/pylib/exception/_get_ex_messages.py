from typing import List

from ._format_traceback import format_traceback


def get_ex_messages(
    ex: BaseException,
    traceback: bool = False,
    tb_reverse: bool = False,
    tb_indent: bool = False,
    no_chain: bool = False,
) -> List[str]:

    """
    Get a list of messages for an exception chain.  The chain starts with the input
    exception and traverses through any other exceptions linked through the `__cause__`
    or `__context__` attributes.

    Args:
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

    message_list = []

    tb_prefix = "    " if tb_indent else ""

    while ex:

        message_list.append(str(ex))

        if traceback:
            tb_message_list = format_traceback(ex, reverse=tb_reverse, prefix=tb_prefix)
            message_list.extend(tb_message_list)

        if no_chain:
            break

        ex = ex.__cause__ or ex.__context__

    return message_list
