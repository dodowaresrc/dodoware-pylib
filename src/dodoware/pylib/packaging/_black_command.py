from dodoware.pylib.packaging._base_command import BaseCommand


class BlackCommand(BaseCommand):
    """
    Run `black` against a source package.
    """

    def __init__(self, tool):

        super().__init__(tool, "black", "check code against black formatting standards")

    def init_syntax(self):

        self.add_folder_args(source=True, output=True)

        self.parser.add_argument(
            "--update", action="store_true", help="update code (just checks by default)"
        )

    def handle_command(self, pr):

        folder_set = self.get_folder_set(pr)

        folder_set.makedirs(output=True)

        args = [folder_set.source_folder]

        if not pr.update:
            args.append("--check")

        process_status = self._run_module(
            module_name="black",
            module_args=args,
            output_folder=folder_set.output_folder)

        if process_status.return_code != 0:
            raise RuntimeError("black failed, check output and retry")
