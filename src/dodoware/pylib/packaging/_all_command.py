from dodoware.pylib.packaging._base_command import BaseCommand


class AllCommand(BaseCommand):
    """
    Run multiple packaging phases in sequence.
    """

    def __init__(self, tool):

        super().__init__(tool, "all", "run all commands in sequence")

    def init_syntax(self):

        self.add_folder_args(source=True, output=True)

        self.parser.add_argument(
            "--publish",
            action="store_true",
            help="publish the package if all other commands are successful",
        )

    def handle_command(self, pr):

        phases = ["black", "pylint", "test", "build"]

        if pr.publish:
            phases.append("publish")

        for phase in phases:

            args = [phase]

            for switch in ("-d", "-t", "-w", "-x"):
                if getattr(pr, switch, None):
                    args.append(switch)

            self.logger.info(f"running phase: {phase}")

            self.tool.run_command(args)
