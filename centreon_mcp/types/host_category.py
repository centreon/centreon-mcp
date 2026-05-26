from typing import ClassVar

from pydantic import BaseModel, Field

from centreon_mcp.types.base import CentreonBaseModel
from centreon_mcp.utils.request import request

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

    @classmethod
    async def get(cls, host_category_id: int) -> "HostCategoryConfiguration":
        """
        Get a host category.
        """
        content = await request("GET", f"{cls.endpoint}/{host_category_id}")
        return cls(**content)

    @classmethod
    async def update(
        cls, host_category_id: int, params: HostCategoryConfigurationFullParams
    ) -> bool:
        """
        Update a host category.
        Return True if successful; otherwise, raise an exception.
        """
        payload = params.model_dump(mode="json", exclude_none=True)
        await request("PUT", f"{cls.endpoint}/{host_category_id}", payload)
        return True

    @classmethod
    async def delete(cls, host_category_id: int) -> bool:
        """
        Delete a host category.
        Return True if successful; otherwise, raise an exception.
        """
        await request("DELETE", f"{cls.endpoint}/{host_category_id}")
        return True
