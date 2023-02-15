from dodoware.pylib.unittest import UnitTestRunner

from dodoware.pylib.packaging._base_command import BaseCommand


class TestCommand(BaseCommand):
    """
    Run unit tests (with optional code coverage) against a source package.
    """

    def __init__(self, tool):

        super().__init__(tool, "test", "run python unit tests")

    def init_syntax(self):

        self.add_folder_args(source=True, output=True, test=True)

        self.parser.add_argument(
            "--failfast",
            action="store_true",
            help="terminate tests if any test fails")

        self.parser.add_argument(
            "--module_pattern",
            help="test case module wildcard pattern (default is '*_test_case.py')")

        self.parser.add_argument(
            "--no_cover", action="store_true", help="do not run code coverage"
        )

        self.parser.add_argument(
            "--test_pattern",
            action="append",
            help="wildcard pattern used to filter test cases",
        )

        self.parser.add_argument(
            "--discover",
            action="store_true",
            help="discover test cases but do not run them",
        )

        self.parser.add_argument(
            "--no_write", help="do not write unittest or code coverage output files"
        )

    def handle_command(self, pr):

        folder_set = self.get_folder_set(pr)

        unit_test_runner = UnitTestRunner(
            package_folder=folder_set.package_folder,
            failfast=pr.failfast,
            module_pattern=pr.module_pattern,
            no_cover=pr.no_cover,
            source_folder=folder_set.source_folder,
            test_folder=folder_set.test_folder,
            test_patterns=pr.test_pattern,
        )

        if pr.discover:
            unit_test_runner.discover()
            return unit_test_runner.get_test_id_list()

        unit_test_runner.run()


        if not pr.no_write:
            unit_test_runner.write_results(output_folder=folder_set.output_folder)

        if (
            unit_test_runner.results.errors or
            unit_test_runner.results.failures or
            unit_test_runner.results.unexpectedSuccesses
        ):
            raise RuntimeError("test failed, check output and retry")

        return unit_test_runner.results
