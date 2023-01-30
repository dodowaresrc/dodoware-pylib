from dodoware.pylib.cmd import Command

class PylintCommand(Command):

    def __init__(self, tool):

        super().__init__(tool, "pylint", "run pylint against python source code")

    def init_syntax(self):

        pass

    def handle_command(self, pr):

        return "PYLINT!!!"
