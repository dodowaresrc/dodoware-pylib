import abc
from contextlib import contextmanager
from threading import Thread, RLock

from dodoware.pylib.exception import ExceptionInfo, get_ex_messages


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
        self._rlock = RLock()

    @contextmanager
    def rlock(self):
        """
        Create a context with the thread reentrant mutex locked.
        """
        with self._rlock:
            yield

    def run(self):
        """
        Run the threading implementation and trap any exceptions.
        """
        try:
            self._run_ex()
        except BaseException as ex:  # pylint: disable=broad-except
            for msg in get_ex_messages(ex, traceback=True):
                print(msg)
            with self.rlock():
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

        with self.rlock():

            if not self._exception:
                return None

            return ExceptionInfo(self._exception)
