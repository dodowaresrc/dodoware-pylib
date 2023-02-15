import json
import os

from dodoware.pylib.terraform._terraform_folder import TerraformFolder
from dodoware.pylib.terraform._terraform_backend import TerraformBackend
from dodoware.pylib.terraform._terraform_prereqs import TerraformPrereqs
from dodoware.pylib.terraform._terraform_service import TerraformService
from dodoware.pylib.terraform._terraform_component import TerraformComponent
from dodoware.pylib.terraform._terraform_project_info import TerraformProjectInfo


class TerraformProject(TerraformFolder):
    """
    A terraform project folder.
    """

    def __init__(self, logger, folder):

        realpath = os.path.realpath(folder)

        self.project_info = self.get_project_info(realpath)

        super().__init__(logger, self.project_info.project, realpath)

        backend = TerraformBackend(self)

        prereqs = TerraformPrereqs(self)

        service = TerraformService(self)

        self._component_map = {
            backend.name: backend,
            prereqs.name: prereqs,
            service.name: service
        }

    @staticmethod
    def get_project_info(project_folder):

        project_info_file = os.path.join(project_folder, "project_info.json")

        with open(project_info_file, mode="r", encoding="UTF-8") as f:
            data = json.load(f)

        return TerraformProjectInfo(**data)

    def get_component(self, name) -> TerraformComponent:
        """
        Get a component by name.

        Args:
            name (str):
                The component name.

        Returns:
            TerraformComponent:
                The component.
        """

        component = self._component_map.get(name)

        if not component:
            raise ValueError(f"component '{name}' not found in project '{self}'")

        return component
