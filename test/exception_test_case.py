import logging
import os
from logging.handlers import BufferingHandler
from test.base_test_case import BaseTestCase

from dodoware.pylib.exception import get_ex_messages, log_ex_messages


class ExceptionTestCase(BaseTestCase):
    """
    Test cases for the `dodoware.pylib.exception` package.
    """

    FILENAME = os.path.basename(__file__)

    # A chain of exception messages raised by test functions in this file.
    NO_BREAKFAST_MESSAGE = "there will be no breakfast today"  # because...
    NO_OMLETTE_MESSAGE = "could not make an omlette"  # because...
    NO_EGGS_MESSAGE = "there are no eggs"  # root cause

    def get_eggs(self):
        """Example function that raises an unchained exception."""
        raise RuntimeError(self.NO_EGGS_MESSAGE)

    def make_omlette(self):
        """Example function that raises a chained exception with chain length 2."""
        try:
            self.get_eggs()
        except RuntimeError as ex:
            raise RuntimeError(self.NO_OMLETTE_MESSAGE) from ex

    def make_breakfast(self):
        """Example function that raises a chained exception with chain length 3."""
        try:
            self.make_omlette()
        except RuntimeError as ex:
            raise RuntimeError(self.NO_BREAKFAST_MESSAGE) from ex

    def test_null(self):
        """Call get_ex_messages() with input `None`."""

        msg_list = get_ex_messages(None)

        self.assertListEqual(msg_list, [])

    def test_simple(self):
        """Simple test case, simulating a single exception with no chaining and no tracebacks."""

        msg_list = None
        msg = "these grapes are sour"

        try:
            raise RuntimeError(msg)
        except RuntimeError as ex:
            msg_list = get_ex_messages(ex)

        self.assertListEqual(msg_list, [msg])

    def test_triple(self):
        """Get messages for an exception chain that is 3 exceptions deep (no tracebacks)."""

        actual = None

        try:
            self.make_breakfast()
        except RuntimeError as ex:
            actual = get_ex_messages(ex)

        expect = [
            self.NO_BREAKFAST_MESSAGE,
            self.NO_OMLETTE_MESSAGE,
            self.NO_EGGS_MESSAGE,
        ]

        self.assertListEqual(actual, expect)

    def test_tracebacks(self):
        """Test exception tracebacks for an exception chain of chain length 3."""

        actual = None

        try:
            self.make_breakfast()
        except RuntimeError as ex:
            actual = get_ex_messages(ex, traceback=True)

        expect = self.load_yaml("test_tracebacks.yaml")

        self.assertListEqual(actual, expect)

    def test_tracebacks_indent(self):
        """Same as test_tracebacks() but indent the exception traceback messages."""

        actual = None

        try:
            self.make_breakfast()
        except RuntimeError as ex:
            actual = get_ex_messages(ex, traceback=True, tb_indent=True)

        expect = self.load_yaml("test_tracebacks_indent.yaml")

        self.assertListEqual(actual, expect)

    def test_tracebacks_reverse(self):
        """Same as test_tracebacks() but reverse the tracebacks."""

        actual = None

        try:
            self.make_breakfast()
        except RuntimeError as ex:
            actual = get_ex_messages(ex, traceback=True, tb_reverse=True)

        expect = self.load_yaml("test_tracebacks_reverse.yaml")

        self.assertListEqual(actual, expect)

    def test_tracebacks_no_chain(self):
        """Same as test_tracebacks() but with 'no_chain' set."""

        actual = None

        try:
            self.make_breakfast()
        except RuntimeError as ex:
            actual = get_ex_messages(ex, no_chain=True)

        expect = [self.NO_BREAKFAST_MESSAGE]

        self.assertListEqual(actual, expect)

    def test_log_ex_messages(self):
        """Test logging exception messages to a logger."""

        logger = logging.getLogger("test_log_ex_messages")

        logger.handlers.clear()

        handler = BufferingHandler(100)

        logger.addHandler(handler)

        try:
            self.make_breakfast()
        except RuntimeError as ex:
            log_ex_messages(logger, ex)

        expect = [
            self.NO_BREAKFAST_MESSAGE,
            self.NO_OMLETTE_MESSAGE,
            self.NO_EGGS_MESSAGE,
        ]

        actual = [x.getMessage() for x in handler.buffer]

        self.assertListEqual(actual, expect)
