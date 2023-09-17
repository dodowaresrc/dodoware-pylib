from contextlib import contextmanager
import sys
from test.base_test_case import BaseTestCase
from datetime import datetime, timedelta
from unittest.mock import patch
import io
import re

from dodoware.pylib.cmd import CommandTool, Command
from dodoware.pylib.logging import get_logger
import logging.handlers
import logging

class AddCommand(Command):

    def __init__(self, tool):

        super().__init__(tool, "add", "add two integers and display the sum")

    def init_syntax(self):

        self.rg.add_argument("n1", help="the first number", type=int)
        self.rg.add_argument("n2", help="the second number", type=int)

    def handle_command(self, pr):

        return pr.n1 + pr.n2
    
class LogCommand(Command):

    LEVELS = (
        ("error", logging.ERROR),
        ("warning", logging.WARNING),
        ("info", logging.INFO),
        ("debug", logging.DEBUG)
    )

    LEVEL_NAMES = [x[0] for x in LEVELS]

    LEVEL_HINT = "|".join(LEVEL_NAMES)

    def __init__(self, tool):

        super().__init__(tool, "log", "log a message")

    def init_syntax(self):

        self.rg.add_argument("--message", help="the message to log")

        self.parser.add_argument("--level", help=f"logging level ({self.LEVEL_HINT})")

    def handle_command(self, pr):


        self.logger.log(logging.ERROR, pr.message)

class SimpleCommandTool(CommandTool):
    
    def __init__(self):

        logger = get_logger("CmdTestCase", debug=True, wide=True)

        logger.handlers.clear()

        handler = logging.handlers.MemoryHandler(1000)

        handler.setLevel(logging.DEBUG)

        logger.addHandler(handler)

        super().__init__(logger)

    def get_command_classes(self):

        return (AddCommand, LogCommand)
    
    @property
    def description(self):
        return "a simple command tool for unit testing"

class CmdTestCase(BaseTestCase):

    def run_tool(self, args):

        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch("sys.stdout", stdout):
            with patch("sys.stderr", stderr):
                tool = SimpleCommandTool()
                result = tool.run_command(args)

        return (result, stdout.getvalue(), stderr.getvalue(), tool.logger.handlers[0].buffer)

    def test_add_simple(self):

        args = ("add", "1", "2")

        (result, stdout, stderr, buffer) = self.run_tool(args)

        self.assertEqual(result, 3)

        self.assertEqual(stdout, "")

        self.assertEqual(stderr, "")

        self.assertEqual(len(buffer), 0)

    def test_log_simple(self):

        args = ("log", "--message", "the eagle has landed", "--level", "error")

        (result, stdout, stderr, buffer) = self.run_tool(args)

        self.assertIsNone(result)

        self.assertEqual(stdout, "")

        self.assertEqual(stderr, "")

        self.assertEqual(len(buffer), 1)

        self.assertEqual(buffer[0].levelno, logging.ERROR)

        self.assertEqual(buffer[0].msg, "the eagle has landed")
