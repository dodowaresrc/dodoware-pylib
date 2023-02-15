from subprocess import PIPE, Popen
from typing import List
from datetime import datetime

from dodoware.pylib.proc._stream_handler import StreamHandler
from dodoware.pylib.proc._stream_settings import StreamSettings
from dodoware.pylib.proc._process_thread import ProcessThread


class ProcessRunner(ProcessThread):
    """
    Start a thread to run a process and handle stdout/stderr.
    """

    def __init__(
        self,
        args: List[str],
        stdout_settings: StreamSettings,
        stderr_settings: StreamSettings,
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

        self.stdout_handler = None
        self.stderr_handler = None

        self._begin = None
        self._end = None

        self._return_code = None

    @property
    def begin_time(self) -> datetime:
        """
        Time when the process started, or `None` if the process
        was not started yet.
        """

        with self.rlock():
            return self._begin

    @property
    def end_time(self) -> datetime:
        """
        Time when the process ended, or `None` if the process
        has not ended yet.
        """

        with self.rlock():
            return self._end

    @property
    def return_code(self) -> int:
        """
        Process return code, or `None` if the process
        has not ended yet.
        """

        with self.rlock():
            return self._return_code

    def _run_ex(self):
        """
        Thread implementation.
        """

        with self.rlock():

            self._begin = datetime.now()

            with Popen(self.args, stdout=PIPE, stderr=PIPE) as process:

                self.stdout_handler = StreamHandler(
                    process.stdout, self.stdout_settings
                )

                self.stderr_handler = StreamHandler(
                    process.stderr, self.stderr_settings
                )

                self.stdout_handler.start()

                self.stderr_handler.start()

                process.wait()

        with self.rlock():

            self._end = datetime.now()

            self._return_code = process.returncode

        self.stdout_handler.join()

        self.stderr_handler.join()
