from dodoware.pylib.terraform._terraform_component import TerraformComponent

class TerraformBackend(TerraformComponent):
    """
    The terraform backend component.
    """

    def __init__(self, project):

        super().__init__(project, "backend", no_backend=True)
