from dodoware.pylib.packaging._base_command import BaseCommand
from dodoware.pylib.unittest import UnitTestRunner


class TestCommand(BaseCommand):
    """
    Run unit tests (with optional code coverage) against a source package.
    """

    def __init__(self, tool):

        super().__init__(tool, "test", "run python unit tests")

    def init_syntax(self):

        self.add_folder_args(source=True, output=True, test=True)

        self.parser.add_argument(
            "--discover", action="store_true", help="discover tests but do not run them"
        )

        self.parser.add_argument(
            "--failfast", action="store_true", help="terminate tests if any test fails"
        )

        self.parser.add_argument(
            "--module_pattern",
            help="test case module wildcard pattern (default is '*_test_case.py')",
        )

        self.parser.add_argument(
            "--no_cover", action="store_true", help="do not run code coverage"
        )

        self.parser.add_argument(
            "--test_pattern",
            action="append",
            help="wildcard pattern used to filter test cases",
        )

        self.parser.add_argument(
            "--no_write", help="do not write unittest or code coverage output files"
        )

        self.parser.add_argument(
            "--min_cover",
            help="minimum code coverage as a percent (default=95)",
            type=float,
            default=95.0,
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
            for test in unit_test_runner.tests:
                print(test)
            return

        unit_test_runner.run()

        if not pr.no_write:
            unit_test_runner.write_results(output_folder=folder_set.output_folder)

        if not pr.no_cover:
            unit_test_runner.coverage_report()

        results = unit_test_runner.results

        if results.errors or results.failures or results.unexpectedSuccesses:
            raise RuntimeError("test failed, check output and retry")

        if not pr.no_cover:
            percent = unit_test_runner.percent
            if percent < pr.min_cover:
                raise RuntimeError(
                    f"coverage failed: minimum={pr.min_cover} actual={percent}"
                )
