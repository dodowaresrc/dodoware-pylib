from datetime import datetime


class ProcessStatus:
    """
    This class is used to consolidate data about a process started by
    a `ProcessRunner` instance.

    Attributes:
        begin (datetime):
            Process begin time, or `None` if the process was never started.
        end (datetime):
            Process end time, or `None` if the process was never started,
            or if it is still running.
        elapsed (float):
            Time difference in seconds between `end` and `begin`, or `None`
            if either `begin` or `end` are None.
        rc (int):
            Process return code, or `None` if the process was never started,
            or if it is still running.
        stdout (bytes):
            Data read from the process stdout stream, if caching was enabled
            on the stdout handler.
        stderr (bytes):
            Data read from the process stderr stream, if caching was enabled
            on the stderr handler.
        runner_ex (Exception):
            Any exception raised within the process runner thread.
        stdout_ex (Exception):
            Any exception raised within the process stdout handler thread.
        stderr_ex (Exception):
            Any exception raised within the process stderr handler thread.
        has_exception (bool):
            `False` if `runner_ex`, `stdout_ex`, and `stderr_ex` are all
            `None`.  True otherwise.
        did_start (bool):
            `True` if the process started, `False` otherwise.
        did_exit (bool):
            `True` if the process exited, `False` otherwise.
    """

    def __init__(self, **kwargs):
        """
        Args:
            This class should only be instantiated by `ProcessRunner`.
        """

        self.begin:datetime = kwargs["datetime"]
        self.end:datetime = kwargs["end"]
        self.rc:int = kwargs["rc"]
        self.stdout:bytes = kwargs["stdout"]
        self.stderr:bytes = kwargs["stderr"]
        self.runner_ex:Exception = kwargs["runner_ex"]
        self.stdout_ex:Exception = kwargs["stdout_ex"]
        self.stderr_ex:Exception = kwargs["stderr_ex"]

        self.elapsed = None
        if self.begin and self.end:
            self.elapsed = (self.end - self.begin).total_seconds()

        self.has_exception = (self.runner_ex or self.stdout_ex or self.stderr_ex)

        self.did_start = bool(self.begin)

        self.did_exit = bool(self.end)
