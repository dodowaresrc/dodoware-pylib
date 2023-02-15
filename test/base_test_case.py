import abc
import io
import json
import os
import re
from contextlib import contextmanager
from unittest import TestCase
from unittest.mock import patch

import yaml


class BaseTestCase(TestCase, metaclass=abc.ABCMeta):
    """
    This class extends `unittest.TestCase` and provides some common functionality
    for test case classes in this package.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.mock_stdout = None

        self.mock_stderr = None

    @contextmanager
    def init_context(self):
        """
        Create a context to capture output written to stdout or stderr during a test.
        """

        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:

            with patch("sys.stderr", new=io.StringIO()) as mock_stderr:

                self.mock_stdout = mock_stdout

                self.mock_stderr = mock_stderr

                yield

    def get_stdout(self):
        """
        Get output written to stdout during a test case, as a single multi-line string.

        Returns:
            str:
                Output written to stdout as a single string.
        """

        if not self.mock_stdout:
            raise RuntimeError(
                "mock stdout not found (maybe init_context() was never called)"
            )

        return self.mock_stdout.getvalue()

    def get_stderr(self):
        """
        Get output written to stderr during a test case, as a single multi-line string.

        Returns:
            str:
                Output written to stderr as a single string.
        """

        if not self.mock_stderr:
            raise RuntimeError(
                "mock stderr not found (maybe init_context() was never called)"
            )

        return self.mock_stderr.getvalue()

    def get_stdout_lines(self):
        """
        Get output written to stdout during a test case, as a list of strings.

        Returns:
            List[str]:
                Lines of output written to stdout during a test case.
        """

        lines = re.split("\r?\n", self.get_stdout())

        if lines and not lines[-1]:
            lines.pop()

        return lines

    def get_stderr_lines(self):
        """
        Get output written to stderr during a test case, as a list of strings.

        Returns:
            List[str]:
                Lines of output written to stderr during a test case.
        """

        lines = re.split("\r?\n", self.get_stderr())

        if lines and not lines[-1]:
            lines.pop()

        return lines

    def get_stdout_json(self):
        """
        Get output written to stdout during a test case, parsed as a JSON document.

        Returns:
            Any:
                Output written to stdout parsed as a JSON document.
        """

        return json.loads(self.get_stdout())

    def get_stderr_json(self):
        """
        Get output written to stderr during a test case, parsed as a JSON document.

        Returns:
            Any:
                Output written to stderr parsed as a JSON document.
        """

        return json.loads(self.get_stderr())

    def get_path(self, filename):
        """
        Get a path to a file in the same folder as the test case class.
        """

        return os.path.join(os.path.dirname(__file__), filename)

    def load_text(self, datafile):
        """
        Load a datafile and return the contents as a single string.
        """

        module_dir = os.path.dirname(__file__)

        datafile_path = os.path.join(module_dir, datafile)

        with open(datafile_path, encoding="UTF-8", mode="r") as f:
            return f.read()

    def load_json(self, datafile):
        """
        Load a datafile and parse the contents as a JSON document.
        """

        module_dir = os.path.dirname(__file__)

        datafile_path = os.path.join(module_dir, datafile)

        with open(datafile_path, encoding="UTF-8", mode="r") as f:
            return json.load(f)

    def load_yaml(self, datafile):
        """
        Load a datafile and parse the contents as a YAML document.
        """

        module_dir = os.path.dirname(__file__)

        datafile_path = os.path.join(module_dir, datafile)

        with open(datafile_path, encoding="UTF-8", mode="r") as f:
            return yaml.safe_load(f)
