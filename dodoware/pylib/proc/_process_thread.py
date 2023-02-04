import abc
from threading import Thread, Lock

from dodoware.pylib.exception import ExceptionInfo

class ProcessThread(Thread, metaclass=abc.ABCMeta):
    """
    Base class for process thread types.
    """

    def __init__(self, *args, **kwargs):
        """
        All we do here is initialize the exception attribute so it can
        be set later if an exception is raised in the threading
        implementation.
        """

        super().__init__(*args, **kwargs)

        self._exception = None
        self._mutex = Lock()

    def run(self):
        """
        Run the threading implementation and trap any exceptions.
        """
        try:
            self._run_ex()
        except BaseException as ex: # pylint: disable=broad-except
            with self._mutex:
                self._exception = ex

    @abc.abstractmethod
    def _run_ex(self):
        """
        Actual threading implementation goes here.
        """

    def get_exception_info(self) -> ExceptionInfo:
        """
        Get information about any exception raised in the threading
        implementation, or `None` if no exception was raised.
        """

        with self._mutex:

            if not self._exception:
                return None

            return ExceptionInfo(self._exception)
