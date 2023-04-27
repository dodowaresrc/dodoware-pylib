from dodoware.pylib.terraform._terraform_base_model import TerraformBaseModel

SHORTENV_MAP = {
    "development": "dev",
    "production": "prod",
    "preview": "pre"
}

class TerraformTags(TerraformBaseModel):
    """
    A collection of common terraform tags.
    """

    base_name: str
    color: str
    component: str
    environment: str
    project: str
    region: str
    short_environment: str
    short_project: str
    short_region: str

    @staticmethod
    def new(project:str, short_project:str, component:str, environment:str, region:str, color:str):
        """
        Factory method.
        """

        short_region = region.replace("-", "")

        short_environment = SHORTENV_MAP.get(environment, environment)

        base_name = "-".join([
            short_project,
            component,
            short_environment,
            short_region,
            color
        ])

        return TerraformTags(
            base_name=base_name,
            color=color,
            component=component,
            environment=environment,
            project=project,
            region=region,
            short_environment=short_environment,
            short_project=short_project,
            short_region=short_region
        )
