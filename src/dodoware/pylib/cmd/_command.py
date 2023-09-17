import abc

from dodoware.pylib.cmd._command_interface import CommandInterface
from dodoware.pylib.cmd._command_tool_interface import CommandToolInterface


class Command(CommandInterface, metaclass=abc.ABCMeta):
    """
    Base class for classes that can handle commands.
    """

    def __init__(self, tool: CommandToolInterface, name: str, hint: str):
        """
        Args:
            tool (CommandToolInterface):
                The command tool this command is associated with.
            name (str):
                The command name.
            hint (str):
                A brief description of what the command does.
        """

        self.tool = tool
        self.logger = self.tool.logger
        self.name = name

        self.parser = self.tool.add_subparser(name, hint)

        self.tool.add_logging_args(self.parser)

        self.parser.set_defaults(handler=self.handle_command)

        self.rg = self.parser.add_argument_group("required arguments")
