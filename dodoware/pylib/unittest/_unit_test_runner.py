import os
from threading import RLock
from typing import List
from unittest import TestLoader, TestResult, TestSuite, TextTestRunner
import json

from coverage import Coverage

from dodoware.pylib.unittest._get_test_id_list import get_test_id_list
from dodoware.pylib.util import path_context
from dodoware.pylib.json import to_jobj

class UnitTestRunner:
    """
    This class can be used to discover and run unit tests, with or without code coverage.
    """

    def __init__(
        self,
        package_folder,
        failfast:bool=False,
        module_pattern:str=None,
        no_cover:bool=False,
        source_folders:List[str]=None,
        test_folder:str=None,
        test_patterns:List[str]=None
    ):
        """
        Args:
            package_folder (str):
                Path to the python package to be tested.
            failfast (bool):
                If set, test runs should fail immediately when the first failure occurs.
            module_pattern (str):
                Wildcard pattern used to identify test case module files.
                Default is `*_test_case.py`.
            no_cover (bool):
                If set, code coverage is not run when test cases are run.
            source_folders (List[str]):
                A list of folder names containing python source code within the
                package folder.  This is for code coverage.
            test_folder (str):
                Name of the folder within the package folder containing unit tests.
                Default is `test`.
            test_patterns (List[str]):
                A list of wildcard patterns used to filter test case discovery.
                Default is no filtering.
        """
        self.package_folder = package_folder

        self.failfast = failfast
        self.module_pattern = module_pattern or "*_test_case.py"
        self.no_cover = no_cover
        self.source_folders = source_folders or ["src"]
        self.start_dir = test_folder or "test"
        self.test_patterns = test_patterns

        self._mutex = RLock()

        self._tests = None
        self._suite = None
        self._coverage = None
        self._results = None

        self.reset()

    @property
    def suite(self) -> TestSuite:
        """
        Get the latest discovered test suite.

        Returns:
            unittest.TestSuite:
                The latest discovered test suite.
        """
        with self._mutex:
            return self._suite

    @property
    def coverage(self) -> Coverage:
        """
        Get the latest coverage results.

        Returns:
            coverage.Coverage:
                The latest coverage results.
        """
        with self._mutex:
            return self._coverage

    @property
    def results(self) -> TestResult:
        """
        Get the latest test results.

        Returns:
            unittest.TestResult:
                The latest test results.
        """
        with self._mutex:
            return self._results

    @property
    def tests(self) -> List[str]:
        """
        Get the latest list of discovered test case IDs.

        Returns:
            List[str]:
                A list of test case IDs.
        """
        with self._mutex:
            return self._tests

    def get_test_id_list(self) -> List[str]:
        """
        Get a list of test IDs from the latest discovered test suite.

        Returns:
            List[str]:
                A list of test IDs.
        """
        with self._mutex:
            return get_test_id_list(self._suite)

    def reset(self) -> None:
        """
        Reset all discovery, testing, and code coverage state.
        """

        with self._mutex:

            self._tests = None
            self._suite = None
            self._coverage = None
            self._results = None

    def discover(self) -> None:
        """
        Discover test cases.  When complete, the test suite can be fetched
        from the `suite` property.
        """

        with self._mutex:

            self.reset()

            with path_context(self.package_folder):

                test_loader = TestLoader()

                test_loader.testNamePatterns = self.test_patterns

                self._suite = test_loader.discover(
                    start_dir=self.start_dir, pattern=self.module_pattern)

                self._tests = get_test_id_list(self._suite)

    def run(self):
        """
        Run test cases.  When complete, test and coverage results can be
        fetched using the `results` and `coverage` properties.
        """

        with self._mutex:
            with path_context(self.package_folder):

                self.discover()

                test_runner = TextTestRunner(failfast=self.failfast)

                if not self.no_cover:
                    self._coverage = Coverage(source=self.source_folders)
                    self._coverage.start()

                self._results = test_runner.run(self.suite)

                if not self.no_cover:
                    self._coverage.stop()

    def write_results(
        self,
        output_folder=None,
        coverage_prefix=None,
        unittest_prefix=None
    ) -> None:
        """
        Write unittest and coverage results to output files.

        Args:
            output_folder (str):
                Output folder for writing files.  If unset, the project folder is used.
            coverage_prefix (str):
                Prefix for coverage output files and folders.  Default is `coverage`.
            unittest_prefix (str):
                Prefix for unittest output files.  Default is `unittest`.
        """

        output_folder = output_folder or self.package_folder
        coverage_prefix = coverage_prefix or "coverage"
        unittest_prefix = unittest_prefix or "unittest"

        coverage_xml = os.path.join(output_folder, f"{coverage_prefix}.xml")
        coverage_json = os.path.join(output_folder, f"{coverage_prefix}.json")
        coverage_txt = os.path.join(output_folder, f"{coverage_prefix}.txt")
        coverage_html = os.path.join(output_folder, f"{coverage_prefix}-html")
        results_json = os.path.join(output_folder, f"{unittest_prefix}-results.json")
        tests_json = os.path.join(output_folder, f"{unittest_prefix}-tests.json")

        with self._mutex:

            if self._coverage:
                self._coverage.xml_report(outfile=coverage_xml)
                self._coverage.json_report(outfile=coverage_json)
                self._coverage.html_report(directory=coverage_html)
                with open(coverage_txt, mode="w", encoding="UTF-8") as f:
                    self._coverage.report(file=f)

            if self._results:
                with open(results_json, mode="w", encoding="UTF-8") as f:
                    json.dump(
                        obj=to_jobj(self._results),
                        fp=f,
                        indent=4,
                        sort_keys=True)

            if self._tests:
                with open(tests_json, mode="w", encoding="UTF-8") as f:
                    json.dump(obj=self._tests, fp=f, indent=4, sort_keys=True)
