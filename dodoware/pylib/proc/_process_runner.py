from subprocess import PIPE, Popen
from typing import List
from datetime import datetime

from dodoware.pylib.proc._stream_handler import StreamHandler
from dodoware.pylib.proc._stream_settings import StreamSettings
from dodoware.pylib.proc._process_status import ProcessStatus
from dodoware.pylib.proc._process_thread import ProcessThread

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

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
    def begin_timestamp(self) -> str:
        """
        Format begin time as a timestamp string.
        """

        begin_time = self.begin_time

        if begin_time:
            return begin_time.strftime(TIMESTAMP_FORMAT)

        return None

    @property
    def end_time(self) -> datetime:
        """
        Time when the process ended, or `None` if the process
        has not ended yet.
        """

        with self.rlock():
            return self._end

    @property
    def end_timestamp(self) -> str:
        """
        Format end time as a timestamp string.
        """

        end_time = self.end_time

        if end_time:
            return end_time.strftime(TIMESTAMP_FORMAT)

        return None

    @property
    def elapsed_time(self) -> float:
        """
        Elapsed time, or `None` if either `begin_time` or `end_time`
        are not set.
        """

        with self.rlock():
            if self._begin and self._end:
                return (self._end - self._begin).total_seconds()
            return None

    @property
    def return_code(self) -> int:
        """
        Process return code, or `None` if the process
        has not ended yet.
        """

        with self.rlock():
            return self._return_code

    def get_status(self) -> ProcessStatus:
        """
        Get the current process status.
        """

        with self.rlock():

            runner_ex = self.exception
            stdout_ex = self.stdout_handler.exception
            stderr_ex = self.stderr_handler.exception

            return ProcessStatus(
                begin_timestamp = self.begin_timestamp,
                end_timestamp = self.end_timestamp,
                elapsed_time = self.elapsed_time,
                return_code = self.return_code,
                runner_exception = (str(runner_ex) if runner_ex else None),
                stdout_exception = (str(stdout_ex) if stdout_ex else None),
                stderr_exception = (str(stderr_ex) if stderr_ex else None),
                stdout_lines = self.stdout_handler.get_lines(),
                stderr_lines = self.stderr_handler.get_lines()
            )

    def _run_ex(self):
        """
        Thread implementation.
        """

        with self.rlock():

            self._begin = datetime.now()

            process = Popen(self.args, stdout=PIPE, stderr=PIPE)

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
