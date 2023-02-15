from typing import List

from dodoware.pylib.cmd import Command, CommandTool
from dodoware.pylib.packaging._black_command import BlackCommand
from dodoware.pylib.packaging._build_command import BuildCommand
from dodoware.pylib.packaging._pylint_command import PylintCommand
from dodoware.pylib.packaging._test_command import TestCommand


class PackagingTool(CommandTool):
    """
    A tool for testing and building python packages.
    """

    def get_command_classes(self) -> List[Command]:

        return (
            BlackCommand,
            BuildCommand,
            PylintCommand,
            TestCommand)

    @property
    def description(self):
        return "a tool for testing and building python packages"
