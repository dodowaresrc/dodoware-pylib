"""
A script to run unit tests with code coverage.
"""

import os
import sys
from argparse import ArgumentParser
from unittest import TestCase, TestLoader, TestSuite, TextTestRunner

from coverage import Coverage


class UnitTestRunner:
    """
    A simple command-line application to run unit tests with code coverage.
    """

    def __init__(self):

        self.parser = ArgumentParser(
            prog=os.path.basename(__file__),
            description="run unit tests with code coverage")

        self.parser.add_argument("--discover", help="only discover unit tests", action="store_true")

        self.parser.add_argument("--nocover", help="do not run code coverage", action="store_true")

        self.parser.add_argument("--filter", help="filter on the test class or method name")

        self.parser.add_argument("--failfast", help="abort tests after first failure", action="store_true")

    def run_command(self, args):
        """
        Run a command
        """

        pr = self.parser.parse_args(args)

        run_coverage = not (pr.nocover or pr.discover)

        if run_coverage:
            cov = Coverage(source=["dodoware"])
            cov.start()

        test_loader = TestLoader()

        if pr.filter:
            test_loader.testNamePatterns = [f"*{pr.filter}*"]

        test_suite = test_loader.discover(start_dir="test", pattern="*TestCase.py")

        if pr.discover:
            test_case_list = self._discover_cases(test_suite)
            for test_case in test_case_list:
                print(test_case.id())
            return

        test_runner = TextTestRunner(failfast=pr.failfast)

        test_result = test_runner.run(test_suite)

        print("test_Result=%s" % test_result)

        if run_coverage:
            cov.stop()
            if not (test_result.errors or test_result.failures):
                cov.xml_report()
                cov.html_report()
                cov.json_report()
                cov.report()

    @staticmethod
    def _discover_cases(test_suite):

        suite_list = [test_suite]
        case_list = []

        while suite_list:
            suite = suite_list.pop()
            for thing in suite:
                if isinstance(thing, TestCase):
                    case_list.append(thing)
                elif isinstance(thing, TestSuite):
                    suite_list.append(thing)

        return case_list

if __name__ == "__main__":
    unit_test_runner = UnitTestRunner()
    unit_test_runner.run_command(sys.argv[1:])
