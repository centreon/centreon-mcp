from typing import ClassVar

from pydantic import BaseModel, Field

from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, ReadMixin, UpdateMixin

DESCRIPTION = {
    "name": "Name of the host severity",
    "alias": "Alias of the host severity",
    "level": "Level for the host severity",
    "icon_id": "ID of the icon for the host severity",
    "comment": "Host severity comment",
    "is_activated": "Indicates whether this host severity is enabled or not",
}


class HostSeverityBaseParams(BaseModel):
    comment: str | None = Field(None, description=DESCRIPTION["comment"])


class HostSeverityFullParams(HostSeverityBaseParams):
    name: str = Field(description=DESCRIPTION["name"])
    alias: str = Field(description=DESCRIPTION["alias"])
    level: int = Field(ge=1, le=127, description=DESCRIPTION["level"])
    icon_id: int = Field(description=DESCRIPTION["icon_id"])
    is_activated: bool = Field(True, description=DESCRIPTION["is_activated"])


class HostSeverityPartialParams(HostSeverityBaseParams):
    name: str | None = Field(None, description=DESCRIPTION["name"])
    alias: str | None = Field(None, description=DESCRIPTION["alias"])
    level: int | None = Field(None, ge=1, le=127, description=DESCRIPTION["level"])
    icon_id: int | None = Field(None, description=DESCRIPTION["icon_id"])
    is_activated: bool | None = Field(None, description=DESCRIPTION["is_activated"])


class HostSeverity(
    BaseModel,
    CreateMixin[HostSeverityFullParams],
    UpdateMixin[HostSeverityFullParams],
    DeleteMixin,
    ReadMixin,
    ListMixin,
):
    endpoint: ClassVar[str] = "configuration/hosts/severities"

    id: int
    name: str
    alias: str
    level: int = Field(ge=1, le=127)
    icon_id: int
    comment: str | None = None
    is_activated: bool
