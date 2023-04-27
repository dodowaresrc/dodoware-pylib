from pydantic import BaseModel, Extra

class TerraformBaseModel(BaseModel):
    """
    A simple extension to `pydantic.BaseModel`.
    """

    class Config:
        """
        Pydantic configuration options.
        """
        extra = Extra.forbid
