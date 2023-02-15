from dodoware.pylib.terraform._terraform_component import TerraformComponent

class TerraformService(TerraformComponent):
    """
    The terraform service component.
    """

    def __init__(self, project):

        super().__init__(project, "service")
