from dodoware.pylib.packaging._base_command import BaseCommand
from dodoware.pylib.unittest import UnitTestRunner


class DiscoverCommand(BaseCommand):
    """
    Discover unit tests but do not run them.
    """

    def __init__(self, tool):

        super().__init__(tool, "discover", "discover unit tests but do not run them")

    def init_syntax(self):

        self.add_folder_args(source=True, output=True, test=True)

    def handle_command(self, pr):

        folder_set = self.get_folder_set(pr)

        unit_test_runner = UnitTestRunner(
            package_folder=folder_set.package_folder,
            source_folder=folder_set.source_folder,
            test_folder=folder_set.test_folder,
        )

        unit_test_runner.discover()

        return unit_test_runner.list_tests()
