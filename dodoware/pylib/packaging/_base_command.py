import abc
import re
import sys
from subprocess import PIPE, Popen

from dodoware.pylib.cmd import Command


class BaseCommand(Command, metaclass=abc.ABCMeta):

    def _run_module(self, module_name, module_args):

        self.logger.info(f"running {module_name}...")

        process_args = [sys.executable, "-m", module_name] + module_args

        process = Popen(process_args, stdout=PIPE, stderr=PIPE)

        (stdout, stderr) = process.communicate()

        self.logger.info(f"{module_name} args:   {module_args}")

        self.logger.info(f"{module_name} rc:     {process.returncode}")

        for line in re.split("\r?\n", str(stdout, encoding="ASCII")):
            self.logger.info(f"{module_name} stdout: {line}")

        for line in re.split("\r?\n", str(stderr, encoding="ASCII")):
            self.logger.info(f"{module_name} stderr: {line}")

        if process.returncode:
            raise Exception(
                f"module '{module_name}' failed, correct problems and retry"
            )
