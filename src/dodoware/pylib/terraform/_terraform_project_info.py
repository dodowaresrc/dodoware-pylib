from dodoware.pylib.terraform._terraform_base_model import TerraformBaseModel

class TerraformProjectInfo(TerraformBaseModel):
    """
    Information about a terraform project.
    """

    project: str
    short_project: str
