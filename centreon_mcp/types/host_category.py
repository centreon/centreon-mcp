from typing import ClassVar

from pydantic import BaseModel, Field

from centreon_mcp.types.base import CentreonBaseModel

DESCRIPTION = {
    "name": "Name for this host category",
    "alias": "Alias for this host category",
    "comment": "Comment for this host category",
    "is_activated": "Whether this host category is enabled or not",
}


class HostCategoryConfigurationBaseParams(BaseModel):
    is_activated: bool | None = Field(None, description=DESCRIPTION["is_activated"])
    comment: str | None = Field(None, description=DESCRIPTION["comment"])


class HostCategoryConfigurationPartialParams(HostCategoryConfigurationBaseParams):
    name: str | None = Field(None, description=DESCRIPTION["name"])
    alias: str | None = Field(None, description=DESCRIPTION["alias"])


class HostCategoryConfigurationFullParams(HostCategoryConfigurationBaseParams):
    name: str = Field(description=DESCRIPTION["name"])
    alias: str = Field(description=DESCRIPTION["alias"])


class HostCategoryConfiguration(CentreonBaseModel):
    endpoint: ClassVar[str] = "configuration/hosts/categories"

    id: int
    name: str
    alias: str
    is_activated: bool
    comment: str | None = None
