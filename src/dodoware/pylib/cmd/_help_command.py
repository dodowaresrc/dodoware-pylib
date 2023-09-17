from dodoware.pylib.cmd._command import Command
from dodoware.pylib.cmd._command_tool_interface import CommandToolInterface


class HelpCommand(Command):
    """
    A command to handle help requests.
    """

    def __init__(self, tool: CommandToolInterface):

        super().__init__(tool, "help", "get usage information")

    def init_syntax(self):

        pass

    def handle_command(self, pr) -> None:

        print()
        print(f"{self.tool}: {self.tool.parser.description}")
        print()
        print(f"usage: {self.tool} COMMAND ARGS")
        print()
        print("the following commands are available:")
        print()

        name_list = sorted(self.tool.command_map.keys())

        maxlen = max(len(x) for x in name_list)

        for name in name_list:
            command = self.tool.command_map[name]
            padded_name = name.ljust(maxlen)
            print(f"    {padded_name}    {command.parser.description}")

        print()
        print(f"for command-specific help, try '{self.tool} COMMAND -h'")
        print()
