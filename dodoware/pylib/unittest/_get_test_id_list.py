from unittest import TestCase, TestSuite
from typing import List

def get_test_id_list(test_suite) -> List[str]:
    """
    Get all test IDs from a test suite.

    Args:
        test_suite (unittest.TestSuite):
            A unittest test suite.

    Returns:
        List[str]:
            A list of test IDs from the test suite.
    """

    if not test_suite:
        return None

    suite_list = [test_suite]

    id_list = []

    while suite_list:

        suite = suite_list.pop()

        for thing in suite:

            if isinstance(thing, TestCase):
                id_list.append(thing.id())

            elif isinstance(thing, TestSuite):
                suite_list.append(thing)

    return id_list
