import os


class FolderSet:
    """
    Some folders of interest to the packaging tool.
    """

    def __init__(
        self,
        package_folder,
        source_folder=None,
        output_folder=None,
        build_folder=None,
        test_folder=None,
    ):
        self.package_folder = package_folder

        self.source_folder = self._get_folder(package_folder, source_folder, "src")

        self.output_folder = self._get_folder(package_folder, output_folder, ".output")

        self.build_folder = self._get_folder(package_folder, build_folder, ".build")

        self.test_folder = self._get_folder(package_folder, test_folder, "test")

    @staticmethod
    def _get_folder(package_folder, sub_folder, default=None):

        if not sub_folder:
            sub_folder = default

        if not os.path.isabs(sub_folder):
            return sub_folder

        return os.path.join(package_folder, sub_folder)

    def makedirs(self, output=False, build=False):
        """
        Create the output and/or build folder if they do not exist.
        """

        if output and not os.path.isdir(self.output_folder):
            os.makedirs(self.output_folder)

        if build and not os.path.isdir(self.build_folder):
            os.makedirs(self.build_folder)
