from dodoware.pylib.packaging._base_command import BaseCommand


class BuildCommand(BaseCommand):
    """
    Build a source package into a wheel.
    """

    def __init__(self, tool):

        super().__init__(tool, "build", "build a python package")

    def init_syntax(self):

        self.add_folder_args(build=True)

        self.parser.add_argument(
            "--no_isolation",
            action="store_true",
            help="do not spawn a python virtual environment")

    def handle_command(self, pr):

        folder_set = self.get_folder_set(pr)

        folder_set.makedirs(build=True, output=True)

        args = [
            "--wheel",
            "--outdir",
            folder_set.build_folder,
            folder_set.package_folder
        ]

        if pr.no_isolation:
            args.append("--no-isolation")

        process_status = self._run_module(
            module_name="build",
            module_args=args,
            output_folder=folder_set.output_folder)

        if process_status.return_code != 0:
            raise RuntimeError("build failed, check output and retry")
