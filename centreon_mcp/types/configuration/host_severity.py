from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseParams
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, PutMixin, ReadMixin

DESCRIPTION = {
    "name": "Name of the host severity",
    "alias": "Alias of the host severity",
    "level": "Level for the host severity",
    "icon_id": "ID of the icon for the host severity",
    "comment": "Host severity comment",
    "is_activated": "Indicates whether this host severity is enabled or not",
}


class HostSeverityOrder(BaseOrder):
    model_type: Literal["host_severity"] = "host_severity"

    field: Literal["name", "alias", "level"] = "name"


class HostSeverityFilter(BaseFilter):
    model_type: Literal["host_severity"] = "host_severity"

    host_severity_id: int | None = Field(default=None, serialization_alias="id $eq")
    host_severity_name: str | None = Field(default=None, serialization_alias="name $eq")
    host_severity_alias: str | None = Field(default=None, serialization_alias="alias $eq")
    min_host_severity_level: int | None = Field(default=None, serialization_alias="level $ge")
    max_host_severity_level: int | None = Field(default=None, serialization_alias="level $le")
    host_severity_is_activated: bool | None = Field(
        default=None, serialization_alias="is_activated $eq"
    )


class HostSeverityBaseParams(BaseParams):
    model_type: Literal["host_severity"] = "host_severity"

    comment: str | None = Field(default=None, description=DESCRIPTION["comment"])


class HostSeverityFullParams(HostSeverityBaseParams):
    name: str = Field(description=DESCRIPTION["name"])
    alias: str = Field(description=DESCRIPTION["alias"])
    level: int = Field(ge=1, le=127, description=DESCRIPTION["level"])
    icon_id: int = Field(description=DESCRIPTION["icon_id"])
    is_activated: bool = Field(True, description=DESCRIPTION["is_activated"])


class HostSeverityPartialParams(HostSeverityBaseParams):
    name: str | None = Field(default=None, description=DESCRIPTION["name"])
    alias: str | None = Field(default=None, description=DESCRIPTION["alias"])
    level: int | None = Field(default=None, ge=1, le=127, description=DESCRIPTION["level"])
    icon_id: int | None = Field(default=None, description=DESCRIPTION["icon_id"])
    is_activated: bool | None = Field(default=None, description=DESCRIPTION["is_activated"])


class HostSeverity(
    BaseModel,
    CreateMixin[HostSeverityFullParams],
    PutMixin[HostSeverityPartialParams, HostSeverityFullParams],
    DeleteMixin,
    ReadMixin,
    ListMixin[HostSeverityFilter, HostSeverityOrder],
):
    endpoint: ClassVar[str] = "configuration/hosts/severities"
    model_type: ClassVar[str] = "host_severity"
    full_params_cls: ClassVar[type[HostSeverityFullParams]] = HostSeverityFullParams

    id: int
    name: str
    alias: str
    level: int = Field(ge=1, le=127)
    icon_id: int
    comment: str | None = None
    is_activated: bool
