from typing import ClassVar

from pydantic import BaseModel, Field

from centreon_mcp.types.base import CentreonBaseModel
from centreon_mcp.utils.request import request


class HostSeverityParams(BaseModel):
    name: str = Field(description="Name of the host severity")
    alias: str | None = Field(default=None, description="Alias of the host severity")
    level: int = Field(ge=1, le=127, description="Level for the host severity")
    icon_id: int = Field(description="ID of the icon for the host severity")


class HostSeverity(CentreonBaseModel):
    endpoint: ClassVar[str] = "configuration/hosts/severities"

    id: int
    name: str
    alias: str
    level: int = Field(ge=1, le=127)
    comment: str | None
    is_activated: bool

    @classmethod
    async def create(cls, params: HostSeverityParams) -> None:
        """
        Create a host severity
        """
        payload = params.model_dump(mode="json")
        await request("POST", cls.endpoint, payload)

    @classmethod
    async def update(cls, host_severity_id: int, params: HostSeverityParams) -> None:
        """
        Partially update a host severity
        """
        payload = params.model_dump(mode="json")
        await request("PATCH", f"{cls.endpoint}/{host_severity_id}", payload)

    @classmethod
    async def delete(cls, host_severity_id: int) -> None:
        """
        Delete a host severity.
        """
        await request("DELETE", f"{cls.endpoint}/{host_severity_id}")
