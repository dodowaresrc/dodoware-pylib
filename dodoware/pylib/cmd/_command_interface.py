import abc
from argparse import Namespace
from typing import Any


class CommandInterface(metaclass=abc.ABCMeta):
    """
    This class defines the command interface needed by command
    tool implementatiions.  Along with `CommandToolInterface`
    this class is intended to prevent circular references
    between the `Command` and `CommandTool` classes.
    """

    @abc.abstractmethod
    def handle_command(self, pr:Namespace) -> Any:
        """
        Handle the command.  To be implmented by subclasses.

        Args:
            pr (argparse.Namespace):
                Parsed command arguments.

        Returns:
            Any:
                The command results.  Each command implementation is free to
                return any datatype including `None`, but best practice is to
                return something that can be directly serialized to JSON.
        """

    @abc.abstractmethod
    def init_syntax(self) -> None:
        """
        Initialize the syntax for this command.  To be implmented by subclasses.
        """
