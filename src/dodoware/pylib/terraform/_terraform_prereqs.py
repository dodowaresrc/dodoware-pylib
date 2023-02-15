from dodoware.pylib.terraform._terraform_component import TerraformComponent

class TerraformPrereqs(TerraformComponent):
    """
    The terraform prereqs component.
    """

    def __init__(self, project):

        super().__init__(project, "prereqs")
