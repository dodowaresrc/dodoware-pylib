import logging
import os
from inspect import currentframe, getframeinfo
from logging.handlers import BufferingHandler
from unittest import TestCase

from dodoware.pylib.exception import get_ex_messages, log_ex_messages

class ExceptionTestCase(TestCase):
    """
    Test cases for the `dodoware.pylib.exception` package.
    """

    FILENAME = os.path.basename(__file__)

    # A chain of exception messages raised by test functions in this file.
    NO_BREAKFAST_MESSAGE = "there will be no breakfast today"  # because...
    NO_OMLETTE_MESSAGE = "could not make an omlette"  # because...
    NO_EGGS_MESSAGE = "there are no eggs"  # root cause

    # Line number within this file where get_eggs() is defined.
    GET_EGGS_LINE = getframeinfo(currentframe()).lineno + 3

    def get_eggs(self):
        """ Example function that raises an unchained exception. """
        raise Exception(self.NO_EGGS_MESSAGE)

    # Line number within this file where make_omlette() is defined.
    MAKE_OMLETTE_LINE = getframeinfo(currentframe()).lineno + 3

    def make_omlette(self):
        """ Example function that raises a chained exception with chain length 2. """
        try:
            self.get_eggs()
        except RuntimeError as ex:
            raise RuntimeError(self.NO_OMLETTE_MESSAGE) from ex

    # Line number within this file where make_breakfast() is defined.
    MAKE_BREAKFAST_LINE = getframeinfo(currentframe()).lineno + 3

    def make_breakfast(self):
        """ Example function that raises a chained exception with chain length 3. """
        try:
            self.make_omlette()
        except RuntimeError as ex:
            raise RuntimeError(self.NO_BREAKFAST_MESSAGE) from ex

    def test_null(self):
        """ Call get_ex_messages() with input `None`. """

        msg_list = get_ex_messages(None)

        self.assertListEqual(msg_list, [])

    def test_simple(self):
        """ Simple test case, simulating a single exception with no chaining and no tracebacks. """

        msg_list = None
        msg = "these grapes are sour"

        try:
            raise Exception(msg)
        except RuntimeError as ex:
            msg_list = get_ex_messages(ex)

        self.assertListEqual(msg_list, [msg])

    def test_triple(self):
        """ Get messages for an exception chain that is 3 exceptions deep (no tracebacks). """

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

    # Line number within this file where test_tracebacks() is defined.
    TEST_TRACEBACKS_LINE = getframeinfo(currentframe()).lineno + 3

    def test_tracebacks(self):
        """ Test exception tracebacks for an exception chain of chain length 3. """

        actual = None

        try:
            self.make_breakfast()
        except RuntimeError as ex:
            actual = get_ex_messages(ex, traceback=True)

        expect = [
            self.NO_BREAKFAST_MESSAGE,
            f"at test_tracebacks line {self.TEST_TRACEBACKS_LINE + 3} in {self.FILENAME}",
            f"at make_breakfast line {self.MAKE_BREAKFAST_LINE + 4} in {self.FILENAME}",
            self.NO_OMLETTE_MESSAGE,
            f"at make_breakfast line {self.MAKE_BREAKFAST_LINE + 3} in {self.FILENAME}",
            f"at make_omlette line {self.MAKE_OMLETTE_LINE + 4} in {self.FILENAME}",
            self.NO_EGGS_MESSAGE,
            f"at make_omlette line {self.MAKE_OMLETTE_LINE + 2} in {self.FILENAME}",
            f"at get_eggs line {self.GET_EGGS_LINE + 1} in {self.FILENAME}"
        ]

        self.assertListEqual(actual, expect)

    # Line number within this file where test_tracebacks_indent() is defined.
    TEST_TRACEBACKS_INDENT_LINE = getframeinfo(currentframe()).lineno + 3

    def test_tracebacks_indent(self):
        """ Same as test_tracebacks() but indent the exception traceback messages. """

        actual = None

        try:
            self.make_breakfast()
        except RuntimeError as ex:
            actual = get_ex_messages(ex, traceback=True, tb_indent=True)

        expect = [
            self.NO_BREAKFAST_MESSAGE,
            f"    at test_tracebacks line {self.TEST_TRACEBACKS_LINE + 3} in {self.FILENAME}",
            f"    at make_breakfast line {self.MAKE_BREAKFAST_LINE + 4} in {self.FILENAME}",
            self.NO_OMLETTE_MESSAGE,
            f"    at make_breakfast line {self.MAKE_BREAKFAST_LINE + 3} in {self.FILENAME}",
            f"    at make_omlette line {self.MAKE_OMLETTE_LINE + 4} in {self.FILENAME}",
            self.NO_EGGS_MESSAGE,
            f"    at make_omlette line {self.MAKE_OMLETTE_LINE + 2} in {self.FILENAME}",
            f"    at get_eggs line {self.GET_EGGS_LINE + 1} in {self.FILENAME}"
        ]

        self.assertListEqual(actual, expect)

    # Line number within this file where test_tracebacks_reverse() is defined.
    TEST_TRACEBACKS_REVERSE_LINE = getframeinfo(currentframe()).lineno + 3

    def test_tracebacks_reverse(self):
        """ Same as test_tracebacks() but reverse the order of exception traceback messages. """

        actual = None

        try:
            self.make_breakfast()
        except RuntimeError as ex:
            actual = get_ex_messages(ex, traceback=True, tb_reverse=True)

        expect = [
            self.NO_BREAKFAST_MESSAGE,
            f"at make_breakfast line {self.MAKE_BREAKFAST_LINE + 4} in {self.FILENAME}",
            f"at test_tracebacks line {self.TEST_TRACEBACKS_LINE + 3} in {self.FILENAME}",
            self.NO_OMLETTE_MESSAGE,
            f"at make_omlette line {self.MAKE_OMLETTE_LINE + 4} in {self.FILENAME}",
            f"at make_breakfast line {self.MAKE_BREAKFAST_LINE + 3} in {self.FILENAME}",
            self.NO_EGGS_MESSAGE,
            f"at get_eggs line {self.GET_EGGS_LINE + 1} in {self.FILENAME}"
            f"at make_omlette line {self.MAKE_OMLETTE_LINE + 2} in {self.FILENAME}",
        ]

        self.assertListEqual(actual, expect)

    def test_tracebacks_no_chain(self):
        """ Same as test_tracebacks() but with 'no_chain' set. """

        actual = None

        try:
            self.make_breakfast()
        except RuntimeError as ex:
            actual = get_ex_messages(ex, no_chain=True)

        expect = [self.NO_BREAKFAST_MESSAGE]

        self.assertListEqual(actual, expect)

    def test_log_ex_messages(self):
        """ Test logging exception messages to a logger. """

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
