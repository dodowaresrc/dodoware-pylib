from dodoware.pylib.packaging._base_command import BaseCommand

class PylintCommand(BaseCommand):

    def __init__(self, tool):

        super().__init__(tool, "pylint", "run pylint against python source code")

    def init_syntax(self):

        self.rg.add_argument(
            "--package_folder",
            required=True,
            help="path to the python package folder")

    def handle_command(self, pr):

        self._run_module("black", ["--check", pr.package_folder])
