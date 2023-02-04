from subprocess import PIPE, Popen
from threading import Lock
from typing import List
from datetime import datetime

from dodoware.pylib.proc._stream_handler import StreamHandler
from dodoware.pylib.proc._stream_settings import StreamSettings
from dodoware.pylib.proc._process_status import ProcessStatus
from dodoware.pylib.proc._process_thread import ProcessThread


class ProcessRunner(ProcessThread):
    """
    Start a thread to run a process and handle stdout/stderr.
    """

    def __init__(
        self,
        args:List[str],
        stdout_settings:StreamSettings,
        stderr_settings:StreamSettings,
    ):
        """
        Args:
            args (List[str]):
                Command-line arguments to start the process.
            stdout_settings (StreamSettings):
                Determines how process stdout is read and handled.
            stderr_settings (StreamSettings):
                Determines how process stderr is read and handled.
        """

        super().__init__()

        self.args = args
        self.stdout_settings = stdout_settings
        self.stderr_settings = stderr_settings

        self._stdout_handler = None
        self._stderr_handler = None

        self._begin = None
        self._end = None
        self._elapsed = None
        self._terminated = None

        self._process = None
        self._rc = None
        self._mutex = Lock()
        self._exception = None

    def _run_ex(self):

        with self._mutex:

            self._begin = datetime.now()

            self._process = Popen(self.args, stdout=PIPE, stderr=PIPE)

            self._stdout_handler = StreamHandler(
                self._process.stdout, self.stdout_settings)

            self._stderr_handler = StreamHandler(
                self._process.stderr, self.stderr_settings)

            self._stdout_handler.start()

            self._stderr_handler.start()

        if self._process:

            self._process.wait()

        with self._mutex:

            self._end = datetime.now()

            self._rc = self._process.returncode

            self._stdout_handler.join()

            self._stderr_handler.join()

    def get_status(self) -> ProcessStatus:
        """
        Get the current status of the process.

        Returns:
            ProcessStatus:
                The process status.
        """

        with self._mutex:
            return ProcessStatus(
                begin = self._begin,
                end = self._end,
                rc = self._rc,
                stdout = self._stdout_handler.get_stash_bytes(),
                stderr = self._stderr_handler.get_stash_bytes(),
                runner_ex = self.get_exception_info(),
                stdout_ex = self._stdout_handler.get_exception_info(),
                stderr_ex = self._stderr_handler.get_exception_info(),
            )
