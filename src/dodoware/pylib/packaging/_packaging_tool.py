from typing import List

from dodoware.pylib.packaging._all_command import AllCommand
from dodoware.pylib.cmd import Command, CommandTool
from dodoware.pylib.packaging._black_command import BlackCommand
from dodoware.pylib.packaging._build_command import BuildCommand
from dodoware.pylib.packaging._pylint_command import PylintCommand
from dodoware.pylib.packaging._test_command import TestCommand
from dodoware.pylib.packaging._discover_command import DiscoverCommand


class PackagingTool(CommandTool):
    """
    A tool for testing and building python packages.
    """

    def get_command_classes(self) -> List[Command]:

        return (
            AllCommand,
            BlackCommand,
            BuildCommand,
            DiscoverCommand,
            PylintCommand,
            TestCommand,
        )

    @property
    def description(self):
        return "a tool for testing and building python packages"
