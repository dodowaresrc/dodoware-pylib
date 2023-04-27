import os

class TerraformFolder:

    def __init__(self, logger, name, folder):

        if not os.path.isabs(folder):
            raise ValueError(f"terraform folder should be absoulte: {folder}")

        if not os.path.isdir(folder):
            raise FileNotFoundError(f"terraform folder not found: {folder}")

        self.name = name
        self.logger = logger
        self.folder = folder

    def __str__(self):
        return self.name

    def get_path(self, name):

        if os.path.isabs(name):
            raise ValueError(f"absolute filename provided: {name}")

        return os.path.join(self.folder, name)

    def check_file(self, name, exist=None):
        """
        Check if a file exists in the folder.

        Args:
            name (str):
                The file name.
            exist (bool):
                If `True`, the file must exist.  If `False`, the file
                must not exist.  Default is `None` which does not care
                either way.
        """

        does_exist = os.path.exists(self.get_path(name))

        if (exist is True) and not does_exist:
            raise FileNotFoundError(f"file '{name}' not found for component '{self}'")

        if (exist is False) and does_exist:
            raise FileExistsError(f"file '{name}' exists for component '{self}'")

        return does_exist

