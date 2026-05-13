from typing import ClassVar

from pydantic import BaseModel, Field

from centreon_mcp.types.base import CentreonBaseModel
from centreon_mcp.utils.request import request

DESCRIPTION = {
    "name": "Name of the host severity",
    "alias": "Alias of the host severity",
    "level": "Level for the host severity",
    "icon_id": "ID of the icon for the host severity",
    "comment": "Host severity comment",
    "is_activated": "Indicates whether this host severity is enabled or not",
}


class HostSeverityParams(BaseModel):
    name: str = Field(description=DESCRIPTION["name"])
    alias: str | None = Field(default=None, description=DESCRIPTION["alias"])
    level: int = Field(ge=1, le=127, description=DESCRIPTION["level"])
    icon_id: int = Field(description=DESCRIPTION["icon_id"])
    comment: str | None = Field(default=None, description=DESCRIPTION["comment"])
    is_activated: bool = Field(default=True, description=DESCRIPTION["is_activated"])


class HostSeverityCreateParams(HostSeverityParams):
    pass


class HostSeverityUpdateParams(HostSeverityParams):
    pass


class HostSeverity(CentreonBaseModel):
    endpoint: ClassVar[str] = "configuration/hosts/severities"

    id: int
    name: str
    alias: str
    level: int = Field(ge=1, le=127)
    icon_id: int
    comment: str | None
    is_activated: bool

    @classmethod
    async def create(cls, params: HostSeverityCreateParams) -> bool:
        """
        Create a host severity.
        Return True if successful; otherwise, raise an exception.
        """
        payload = params.model_dump(mode="json")
        await request("POST", cls.endpoint, payload)
        return True

    @classmethod
    async def update(cls, host_severity_id: int, params: HostSeverityUpdateParams) -> bool:
        """
        Partially update a host severity.
        Return True if successful; otherwise, raise an exception.
        """
        payload = params.model_dump(mode="json", exclude_none=True)
        await request("PUT", f"{cls.endpoint}/{host_severity_id}", payload)
        return True

    @classmethod
    async def delete(cls, host_severity_id: int) -> bool:
        """
        Delete a host severity.
        Return True if successful; otherwise, raise an exception.
        """
        await request("DELETE", f"{cls.endpoint}/{host_severity_id}")
        return True
