from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseParams
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, PutMixin, ReadMixin

DESCRIPTION = {
    "name": "Name of the service severity",
    "alias": "Alias of the service severity",
    "level": "Level for the service severity",
    "icon_id": "ID of the icon for the service severity",
    "is_activated": "Indicates whether this service severity is enabled or not",
}


class ServiceSeverityOrder(BaseOrder):
    model_type: Literal["service_severity"] = "service_severity"

    field: Literal["name", "alias", "level"] = "name"


class ServiceSeverityFilter(BaseFilter):
    model_type: Literal["service_severity"] = "service_severity"

    service_severity_id: int | None = Field(default=None, serialization_alias="id $eq")
    service_severity_name: str | None = Field(default=None, serialization_alias="name $eq")
    service_severity_alias: str | None = Field(default=None, serialization_alias="alias $eq")
    min_service_severity_level: int | None = Field(default=None, serialization_alias="level $ge")
    max_service_severity_level: int | None = Field(default=None, serialization_alias="level $le")
    service_service_is_activated: bool | None = Field(
        default=None, serialization_alias="is_activated $eq"
    )


class ServiceSeverityBaseParams(BaseParams):
    model_type: Literal["service_severity"] = "service_severity"

    is_activated: bool | None = Field(default=None, description=DESCRIPTION["is_activated"])


class ServiceSeverityFullParams(ServiceSeverityBaseParams):
    name: str = Field(description=DESCRIPTION["name"])
    alias: str = Field(description=DESCRIPTION["alias"])
    level: int = Field(ge=1, le=127, description=DESCRIPTION["level"])
    icon_id: int = Field(description=DESCRIPTION["icon_id"])


class ServiceSeverityPartialParams(ServiceSeverityBaseParams):
    name: str | None = Field(default=None, description=DESCRIPTION["name"])
    alias: str | None = Field(default=None, description=DESCRIPTION["alias"])
    level: int | None = Field(default=None, ge=1, le=127, description=DESCRIPTION["level"])
    icon_id: int | None = Field(default=None, description=DESCRIPTION["icon_id"])


class ServiceSeverity(
    BaseModel,
    CreateMixin[ServiceSeverityFullParams],
    PutMixin[ServiceSeverityPartialParams, ServiceSeverityFullParams],
    DeleteMixin,
    ReadMixin,
    ListMixin[ServiceSeverityFilter, ServiceSeverityOrder],
):
    endpoint: ClassVar[str] = "configuration/services/severities"
    model_type: ClassVar[str] = "service_severity"
    full_params_cls: ClassVar[type[ServiceSeverityFullParams]] = ServiceSeverityFullParams

    id: int
    name: str
    alias: str
    level: int = Field(ge=1, le=127)
    icon_id: int
    is_activated: bool
