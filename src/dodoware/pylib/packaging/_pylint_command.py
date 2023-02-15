from dodoware.pylib.packaging._base_command import BaseCommand


class PylintCommand(BaseCommand):
    """
    Run `pylint` against a source package.
    """

    def __init__(self, tool):

        super().__init__(tool, "pylint", "run pylint against python source code")

    def init_syntax(self):

        self.add_folder_args(source=True, output=True)

    def handle_command(self, pr):

        folder_set = self.get_folder_set(pr)

        folder_set.makedirs(output=True)

        process_status = self._run_module(
            module_name="pylint",
            module_args=[folder_set.source_folder],
            output_folder=folder_set.output_folder)

        if process_status.return_code != 0:
            raise RuntimeError("pylint failed, check output and retry")
