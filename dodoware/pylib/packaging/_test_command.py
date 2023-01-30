import os
from dodoware.pylib.cmd import Command
from dodoware.pylib.unittest import UnitTestRunner

class TestCommand(Command):
    """
    A command to run unit tests with code coverage.
    """

    def __init__(self, tool):

        super().__init__(tool, "test", "run python unit tests")

    def init_syntax(self):

        self.rg.add_argument(
            "--package_folder",
            required=True,
            help="path to the python package folder")

        self.parser.add_argument(
            "--failfast",
            action="store_true",
            help="terminate tests if any test fails")

        self.parser.add_argument(
            "--module_pattern",
            help="test case module wildcard pattern (default is '*_test_case.py')")

        self.parser.add_argument(
            "--no_cover",
            action="store_true",
            help="do not run code coverage")

        self.parser.add_argument(
            "--source_folder",
            action="append",
            help="source code folder names (for code coverage)")

        self.parser.add_argument(
            "--test_folder",
            help="folder name containing test cases (default is 'test')")

        self.parser.add_argument(
            "--test_pattern",
            action="append",
            help="wildcard pattern used to filter test cases")

        self.parser.add_argument(
            "--discover",
            action="store_true",
            help="discover test cases but do not run them")

        self.parser.add_argument(
            "--output_folder",
            help="path to output folder (default is `package_folder/results`)")

        self.parser.add_argument(
            "--no_write",
            help="do not write unittest or code coverage output files")

    def handle_command(self, pr):

        unit_test_runner = UnitTestRunner(
            package_folder=pr.package_folder,
            failfast=pr.failfast,
            module_pattern=pr.module_pattern,
            no_cover=pr.no_cover,
            source_folders=pr.source_folder,
            test_folder=pr.test_folder,
            test_patterns=pr.test_pattern)

        if pr.discover:

            unit_test_runner.discover()

            return unit_test_runner.get_test_id_list()

        unit_test_runner.run()

        if not pr.no_write:

            output_folder = (
                pr.output_folder or os.path.join(pr.package_folder, "results")
            )

            unit_test_runner.write_results(output_folder=output_folder)
