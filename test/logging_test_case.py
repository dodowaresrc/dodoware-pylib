import re
from datetime import datetime, timedelta
from test.base_test_case import BaseTestCase

from dodoware.pylib.logging import get_logger, init_logger

RE_TIMESTAMP = r"(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)"
RE_WHENCE = r"\s*\w+\.\w+:\d+\s*"
RE_LEVEL = r"([A-Z]+)\s*"
RE_MESSAGE = r"\| (.*)"
RE_WIDE = re.compile(f"{RE_TIMESTAMP} {RE_LEVEL} {RE_MESSAGE}")
RE_XTRA = re.compile(f"{RE_TIMESTAMP} {RE_LEVEL} {RE_WHENCE} {RE_MESSAGE}")

STRPTIME_FMT = r"%Y-%m-%d %H:%M:%S"


class LoggingTestCase(BaseTestCase):
    """Test cases for the `dodoware.pylib.logging` package."""

    def _log_simple_messages(self, **kwargs):

        with self.init_context():

            logger = get_logger("LoggingTestCase", **kwargs)

        logger.error("error")
        logger.warning("warning")
        logger.info("info")
        logger.debug("debug")

        return (self.get_stdout_lines(), self.get_stderr_lines())

    def test_get_logger_defaults(self):
        """Get a logger with default settings."""

        (actual_stdout, actual_stderr) = self._log_simple_messages()

        self.assertListEqual(actual_stdout, [])

        self.assertListEqual(actual_stderr, ["error", "warning", "info"])

    def test_get_logger_debug(self):
        """Get a logger with the debug flag set."""

        (actual_stdout, actual_stderr) = self._log_simple_messages(debug=True)

        self.assertListEqual(actual_stdout, [])

        self.assertListEqual(actual_stderr, ["error", "warning", "info", "debug"])

    def _check_log_output_line(
        self,
        line: str,
        t1: datetime,
        t2: datetime,
        level: str,
        message: str,
        xtra: bool = False,
    ):

        regex = RE_XTRA if xtra else RE_WIDE

        m = regex.match(line)

        self.assertIsNotNone(m)

        t = datetime.strptime(m.group(1), STRPTIME_FMT)

        self.assertGreaterEqual(t, t1)

        self.assertLessEqual(t, t2)

        self.assertEqual(m.group(2), level)

        self.assertEqual(m.group(3), message)

    def test_get_logger_wide_and_xtra(self):
        """Get a logger with the wide and xtra flags set in sequence."""

        for xtra in (False, True):

            t1 = datetime.now() - timedelta(seconds=1)

            (actual_stdout, actual_stderr) = self._log_simple_messages(
                wide=True, xtra=xtra
            )

            t2 = datetime.now() + timedelta(seconds=1)

            self.assertListEqual(actual_stdout, [])

            self.assertEqual(len(actual_stderr), 3)

            self._check_log_output_line(
                actual_stderr[0], t1, t2, "ERROR", "error", xtra=xtra
            )

            self._check_log_output_line(
                actual_stderr[1], t1, t2, "WARN", "warning", xtra=xtra
            )

            self._check_log_output_line(
                actual_stderr[2], t1, t2, "INFO", "info", xtra=xtra
            )

    def test_init_logger_options(self):
        """Test all permutations of `init_logger()`."""

        for debug in ([], ["-d"]):

            for wide in ([], ["-w"]):

                for xtra in ([], ["-x"]):

                    with self.init_context():

                        logger = init_logger("xyz", debug + wide + xtra)

                        logger.info("info")

                        logger.debug("debug")

                    stderr_messages = self.get_stderr_lines()

                    self.assertEqual(len(stderr_messages), (2 if debug else 1))

                    if xtra:
                        self.assertRegex(stderr_messages[0], RE_XTRA)
                    elif wide:
                        self.assertRegex(stderr_messages[0], RE_WIDE)
                    else:
                        self.assertEqual(stderr_messages[0], "info")
