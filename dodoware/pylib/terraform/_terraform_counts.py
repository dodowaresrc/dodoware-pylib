import os
import re

from dodoware.pylib.terraform._terraform_base_model import TerraformBaseModel

COUNTS_REGEX = re.compile(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy.")

NOOP_REGEX = re.compile("No changes. Your infrastructure matches the configuration.")

class TerraformCounts(TerraformBaseModel):
    """
    Counts of resources to be created, modified, and destroyed.
    Parsed from `terraform plan` output.
    """

    add: int
    change: int
    destroy: int

    @staticmethod
    def load(path):
        """
        Load terraform counts from a `terraform plan` stdout file.

        Args:
            path (str):
                Path to the `terraform plan` stdout file.
        """

        if not os.path.isfile(path):
            raise FileNotFoundError(f"terraform plan stdout file not found: {path}")

        with open(path, mode="r", encoding="UTF-8") as f:

            while True:

                line = f.readline()

                if not line:
                    break

                m = COUNTS_REGEX.match(line)

                if m:
                    add = int(m.group(1))
                    change = int(m.group(2))
                    destroy = int(m.group(3))
                    return TerraformCounts(add=add, change=change, destroy=destroy)

                if NOOP_REGEX.match(line):
                    return TerraformCounts(add=0, change=0, destroy=0)

            raise RuntimeError(f"terraform counts not found in file: {path}") 
