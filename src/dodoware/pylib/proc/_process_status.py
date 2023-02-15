from dodoware.pylib.proc._process_runner import ProcessRunner


class ProcessStatus:
    """
    This class is used to consolidate data about a process started by
    a `ProcessRunner` instance.
    """

    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, process_runner: ProcessRunner):
        """
        Args:
            process_runner (ProcessRunner):
                The source of process information.
        """

        begin_time = process_runner.begin_time
        end_time = process_runner.end_time

        self.begin_timestamp = (
            begin_time.strftime(self.TIMESTAMP_FORMAT) if begin_time else None
        )

        self.end_timestamp = (
            end_time.strftime(self.TIMESTAMP_FORMAT) if begin_time else None
        )

        self.elapsed_seconds = (
            (end_time - begin_time).total_seconds()
            if (begin_time and end_time)
            else None
        )

        self.return_code = process_runner.return_code

        self.runner_exception = process_runner.get_exception_info()

        self.stdout_exception = process_runner.stdout_handler.get_exception_info()

        self.stderr_exception = process_runner.stderr_handler.get_exception_info()

        self.stdout_lines = process_runner.stdout_handler.get_lines()

        self.stderr_lines = process_runner.stderr_handler.get_lines()
