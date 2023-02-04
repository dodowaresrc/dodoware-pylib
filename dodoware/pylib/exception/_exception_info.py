from dodoware.pylib.exception._format_traceback import format_traceback

class ExceptionInfo:
    """
    This class is used to collect information about an exception
    that can be serialized directly to JSON.
    """

    def __init__(self, exception:BaseException):

        self.class_name = type(exception).__name__
        self.message = str(exception)
        self.traceback = format_traceback(exception)
        self.cause = None
        self.context = None

        if (
            hasattr(exception, "__cause__") and
            isinstance(exception.__cause__, BaseException)
        ):
            self.cause = ExceptionInfo(exception.__cause__)

        if (
            hasattr(exception, "__context__") and
            isinstance(exception.__context__, BaseException)
        ):
            self.cause = ExceptionInfo(exception.__context__)
