import abc
from argparse import ArgumentParser
from logging import Logger
from typing import Dict

from dodoware.pylib.cmd._command_interface import CommandInterface


class CommandToolInterface(metaclass=abc.ABCMeta):
    """
    This class defines the command tool interface needed by
    indivdual command classes.  Along with `CommandInterface`
    this class is intended to prevent circular references
    between the `Command` and `CommandTool` classes.
    """

    @staticmethod
    @abc.abstractmethod
    def add_logging_args(parser: ArgumentParser) -> None:
        """
        Static helper method to add a common set of logging args
        to a command subparser, or the main command tool parser.
        """

    @abc.abstractmethod
    def add_subparser(self, name, description) -> ArgumentParser:
        """
        Add a subparser for a command.

        Args:
            name (str):
                The command name.
            description (str):
                A brief command description.

        Returns:
            ArgumentParser:
                The command subparser.
        """

    @property
    @abc.abstractmethod
    def logger(self) -> Logger:
        """
        Get the command tool logger.
        """

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """
        Get a brief description of the command tool for usage text purposes.
        """

    @property
    @abc.abstractmethod
    def command_map(self) -> Dict[str, CommandInterface]:
        """
        Get the command tool command map.
        """
