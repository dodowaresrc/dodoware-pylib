from typing import List
import os
import traceback

def format_traceback(
    ex:BaseException,
    reverse:bool=False,
    prefix:str=None
) -> List[str]:

    """
    Get a list of messages representing an exception traceback.  The default ordering
    traces the stack from the program entry point to the frame where the exception is
    raised.  Set the 'reverse' flag to start where the exception is raised then bubble
    up the stack to the program entry point.

    Args:
        ex (BaseException):
            The input exception.
        reverse (bool):
            If set, reverse the order of traceback messages.
        prefix (str):
            Optional prefix added to each traceback message.

    Returns:
        List[str]:
            A list of formatted exception traceback messages.
    """

    message_list = []

    if not prefix:
        prefix = ""


    for frame in traceback.extract_tb(ex.__traceback__):

        fname = os.path.basename(frame.filename)

        message = f"{prefix}at {frame.name} line {frame.lineno} in {fname}"

        message_list.append(message)

    if reverse:
        message_list.reverse()

    return message_list
