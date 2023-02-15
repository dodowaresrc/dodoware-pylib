import abc
import json
import sys
from argparse import ArgumentParser, Namespace
from logging import Logger
from typing import Any, Dict, List

from dodoware.pylib.json import to_jobj
from dodoware.pylib.cmd._command_interface import CommandInterface
from dodoware.pylib.cmd._help_formatter import HelpFormatter
from dodoware.pylib.cmd._command_tool_interface import CommandToolInterface
from dodoware.pylib.cmd._help_command import HelpCommand
from dodoware.pylib.exception import log_ex_messages
from dodoware.pylib.logging import init_logger


class CommandTool(CommandToolInterface):
    """
    Base class for command tools that use `argparse` for command-line
    argument parsing, and a common design pattern for handling commands.
    """

    @abc.abstractmethod
    def get_command_classes(self) -> List[CommandInterface]:
        """
        Get a list of command classes supported by this command tool.
        To be implemented by subclasses.
        """
        return None

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def command_map(self) -> Dict[str, CommandInterface]:
        return self._command_map

    def __str__(self):

        return type(self).__name__

    def __init__(self, logger):
        """
        Args:
            logger (logging.Logger):
                The logger to use for all logged messages.
        """

        self._logger = logger

        self.parser = ArgumentParser(
            description=self.description, prog=str(self), formatter_class=HelpFormatter
        )

        self.add_logging_args(self.parser)

        self.parser.set_defaults(handler=self.handle_help)

        self.subparsers = self.parser.add_subparsers()

        self._command_map = {}

        self._command_map["help"] = HelpCommand(self)

        for command_class in self.get_command_classes():

            command = command_class(self)

            command.init_syntax()

            self._command_map[command.name] = command

    def add_subparser(self, name, description) -> ArgumentParser:

        return self.subparsers.add_parser(
            name, description=description, formatter_class=HelpFormatter
        )

    @staticmethod
    def add_logging_args(parser: ArgumentParser) -> None:
        """
        Helper method to add a common set of logging arguments to the main
        command tool parser, and also all command subparsers.
        """

        group = parser.add_argument_group("logging args")
        group.add_argument("-d", action="store_true", help="enable debug logging")
        group.add_argument(
            "-t", action="store_true", help="enable full exception tracebacks"
        )
        group.add_argument("-w", action="store_true", help="enable wide log messages")
        group.add_argument(
            "-x", action="store_true", help="enable extra-wide log messages"
        )

    def handle_help(self, pr: Namespace) -> Any:
        """
        Handle a general help command.

        Args:
            pr (argparse.Namespace):
                Parsed command arguments.

        Returns:
            Any:
                The return value of the help handler (usually `None`).
        """

        return self.command_map.get("help").handle_command(pr)

    def run_command(self, args: List[str]) -> Any:
        """
        Run a command and return the command result to the caller.

        Args (List[str]):
            The command to run.

        Returns:
            Any:
                The return value of the command handler.
        """

        pr = self.parser.parse_args(args)

        return pr.handler(pr)

    def run_tool(self, args) -> None:
        """
        Run a command and display the command result on the console.

        Args (List[str]):
            The command to run.
        """

        try:

            result = self.run_command(args)

            if isinstance(result, (str, int, bool, float)):

                print(result)

            elif result is not None:

                try:
                    print(json.dumps(to_jobj(result), indent=4, sort_keys=True))
                except Exception as ex:  # pylint: disable=broad-except
                    self.logger.exception(ex)
                    print(str(result))

        except Exception as ex:

            log_ex_messages(self.logger, ex, traceback=("-t" in args))

            raise SystemExit(1) from ex

    @classmethod
    def main(cls) -> None:
        """
        Static entry point.
        """

        args = sys.argv[1:]

        logger = init_logger(name=cls.__name__, args=args)

        tool = cls(logger)

        tool.run_tool(args)
