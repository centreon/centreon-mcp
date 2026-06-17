from enum import IntEnum
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

ResourceType = Literal["host", "service"]
StatusType = Literal["soft", "hard"]
HostStatus = Literal["UP", "DOWN", "UNREACHABLE", "PENDING"]
ServiceStatus = Literal["OK", "WARNING", "CRITICAL", "UNKNOWN", "PENDING"]
ResourceStatus = HostStatus | ServiceStatus


class HostState(IntEnum):
    UP = 0
    DOWN = 1
    UNREACHABLE = 2
    PENDING = 4


class ServiceState(IntEnum):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3
    PENDING = 4


class Status(BaseModel):
    code: int
    name: ResourceStatus
    severity_code: int


class EnablementStatus(IntEnum):
    STATUS_DISABLED = 0
    STATUS_ENABLED = 1
    STATUS_DEFAULT = 2


class StatusCount(BaseModel):
    pending: int
    total: int

    @model_validator(mode="before")
    @classmethod
    def flatten(cls, data: dict[str, Any]):
        return {
            "total": data.pop("total"),
            **{status: count["total"] for status, count in data.items()},
        }


class BaseResource(BaseModel):
    type: ResourceType
    resource_id: int = Field(..., serialization_alias="id")
    host_id: int

    def dump(self) -> dict[str, Any]:
        """
        Dump the resource to a dict with the expected format for the API.
        """
        return {
            "parent": {"id": self.host_id},
            **self.model_dump(mode="json", by_alias=True, exclude={"host_id"}),
        }


class Link(BaseModel):
    """
    Minimal representation of a related resource.
    Used to represent linked entities embedded in API responses.
    """

    id: int
    name: str
