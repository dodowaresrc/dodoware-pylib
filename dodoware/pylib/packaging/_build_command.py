from dodoware.pylib.cmd import Command

class BuildCommand(Command):

    def __init__(self, tool):

        super().__init__(tool, "build", "build a python package")

    def init_syntax(self):

        pass

    def handle_command(self, pr):

        return "BUILD!!!"
