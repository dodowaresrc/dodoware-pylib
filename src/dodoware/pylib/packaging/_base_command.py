import abc
import logging
import os
import sys

from dodoware.pylib.cmd import Command
from dodoware.pylib.packaging._folder_set import FolderSet
from dodoware.pylib.proc import ProcessRunner, ProcessStatus, StreamSettings


class BaseCommand(Command, metaclass=abc.ABCMeta):
    """
    Base command for the packaging tool.
    """

    def _run_module(self, module_name, module_args=None, output_folder=None):

        args = [sys.executable, "-m", module_name] + (module_args or [])

        stdout_file = (
            os.path.join(output_folder, f"{module_name}.stdout")
            if output_folder
            else None
        )

        stderr_file = (
            os.path.join(output_folder, f"{module_name}.stderr")
            if output_folder
            else None
        )

        stdout_settings = StreamSettings(
            logger=self.logger,
            log_prefix="stdout: ",
            log_level=logging.INFO,
            outfile=stdout_file,
            overwrite=True)

        stderr_settings = StreamSettings(
            logger=self.logger,
            log_prefix="stderr: ",
            log_level=logging.INFO,
            outfile=stderr_file,
            overwrite=True)

        process_runner = ProcessRunner(args, stdout_settings, stderr_settings)

        process_runner.start()

        process_runner.join()

        return ProcessStatus(process_runner)

    def add_folder_args(self, output=False, build=False, source=False, test=False):
        """
        Add some common folder arguments.
        """

        self.parser.add_argument(
            "--package_folder",
            help="python package folder (default is current folder)"
        )

        if output:
            self.parser.add_argument(
                "--output_folder",
                help="output folder (default='.output')"
            )

        if build:
            self.parser.add_argument(
                "--build_folder",
                help="build folder (default='.build')"
            )

        if source:
            self.parser.add_argument(
                "--source_folder",
                help="source folder (default='src')"
            )

        if test:
            self.parser.add_argument(
                "--test_folder",
                help="test folder (default='test')"
            )

    def get_folder_set(self, pr):
        """
        Get some common folder argument values.
        """

        package_folder = getattr(pr, "output_folder", None) or os.getcwd()

        source_folder = getattr(pr, "source_folder", None)

        build_folder = getattr(pr, "build_folder", None)

        output_folder = getattr(pr, "output_folder", None)

        return FolderSet(
            package_folder,
            source_folder=source_folder,
            build_folder=build_folder,
            output_folder=output_folder)
