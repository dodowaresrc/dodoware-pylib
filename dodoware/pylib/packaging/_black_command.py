from dodoware.pylib.cmd import Command

class BlackCommand(Command):

    def __init__(self, tool):

        super().__init__(tool, "black", "check code against black formatting standards")

    def init_syntax(self):

        pass

    def handle_command(self, pr):

        return "BLACK!!!"
