import sys
from test.base_test_case import BaseTestCase
from datetime import datetime, timedelta
from unittest.mock import patch
import io
import re

from dodoware.pylib.proc import ProcessRunner, StreamSettings
from dodoware.pylib.logging import get_logger
import logging.handlers
import logging


class NonClosingBytesIO(io.BytesIO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def close(self, *args, **kwargs):
        pass


class ProcessTestCase(BaseTestCase):
    """
    Test cases for the `dodoware.pylib.proc` package.
    """

    def _get_logger(self, debug=False, wide=False, xtra=False):

        logger = get_logger("ProcessTestCase", debug=debug, wide=wide, xtra=xtra)

        logger.handlers.clear()

        handler = logging.handlers.MemoryHandler(1000)

        handler.setLevel(logging.DEBUG if debug else logging.INFO)

        logger.addHandler(handler)

        return (logger, handler)

    def _run_python(self, script, stdout_settings, stderr_settings):

        args = [sys.executable, self.get_path(script)]

        return self._run_process(args, stdout_settings, stderr_settings)

    def _run_process(self, args, stdout_settings, stderr_settings):

        t0 = datetime.now() - timedelta(seconds=1)

        process_runner = ProcessRunner(args, stdout_settings, stderr_settings)

        process_runner.start()

        process_runner.join()

        t1 = datetime.now() + timedelta(seconds=1)

        process_status = process_runner.get_status()

        begin_time = datetime.fromisoformat(process_status.begin_timestamp)

        end_time = datetime.fromisoformat(process_status.end_timestamp)

        self.assertGreaterEqual(begin_time, t0)

        self.assertLessEqual(end_time, t1)

        return (process_runner, process_status)

    def test_simple_stash(self):
        """
        Run a simple script and stash the output.
        """

        (_runner, status) = self._run_python(
            "test_process_simple.py",
            StreamSettings(max_stash_kb=1),
            StreamSettings(max_stash_kb=1),
        )

        self.assertEqual(status.return_code, 0)
        self.assertIsNone(status.runner_exception)
        self.assertIsNone(status.stdout_exception)
        self.assertIsNone(status.stderr_exception)
        self.assertListEqual(status.stdout_lines, ["0", "1", "2", "3", "4", ""])
        self.assertListEqual(status.stderr_lines, [])

    def test_simple_logger(self):
        """
        Run a simple script and log the output.
        """

        (logger, handler) = self._get_logger()

        (_runner, status) = self._run_python(
            "test_process_simple.py",
            StreamSettings(logger=logger, log_level=logging.INFO),
            StreamSettings(logger=logger, log_level=logging.ERROR),
        )

        self.assertEqual(status.return_code, 0)
        self.assertIsNone(status.runner_exception)
        self.assertIsNone(status.stdout_exception)
        self.assertIsNone(status.stderr_exception)
        self.assertIsNone(status.stdout_lines)
        self.assertIsNone(status.stderr_lines)
        self.assertEqual(len(handler.buffer), 5)

        actual_list = [x.getMessage() for x in handler.buffer]

        expect_list = ["0", "1", "2", "3", "4"]

        self.assertListEqual(actual_list, expect_list)

    def test_simple_outfile(self):
        """
        Run a simple script and write output to a file.
        """

        (logger, handler) = self._get_logger()

        mock_stdout = NonClosingBytesIO()

        with patch("builtins.open", return_value=mock_stdout) as mock_open:

            (runner, status) = self._run_python(
                "test_process_simple.py",
                StreamSettings(outfile="stdout.out"),
                StreamSettings(),
            )

        mock_open.assert_called_once_with("stdout.out", mode="wb")

        actual_lines = re.split("\r?\n", str(mock_stdout.getvalue(), "UTF-8"))

        expect_lines = ["0", "1", "2", "3", "4", ""]

        self.assertEqual(actual_lines, expect_lines)
