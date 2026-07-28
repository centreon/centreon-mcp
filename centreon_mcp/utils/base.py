from collections.abc import Sequence
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


class BaseOrder(BaseModel):
    model_type: str

    order: Literal["ASC", "DESC"] = "ASC"

    def check(self, model_type: str):
        """
        Raise ValueError if model_type does not match the order expected model_type.
        """
        if self.model_type != model_type:
            raise ValueError(
                f"model_type {model_type!r} does not match order.model_type {self.model_type!r}"
            )


class BaseFilter(BaseModel):
    model_type: str

    @staticmethod
    def join(filters: Sequence["BaseFilter"] | None) -> dict:
        """
        Join multiple filters conditions using OR operator.
        """
        return {"$or": [{"$and": f.conditions} for f in filters if f.conditions]} if filters else {}

    @property
    def conditions(self) -> list:
        """
        Generate list of conditions dictionary for filtering.
        """
        return [
            {name: {operator: value}}
            for (name, operator), value in {
                tuple(condition.split()): value
                for condition, value in self.model_dump(
                    mode="json", by_alias=True, exclude={"model_type"}
                ).items()
                if value is not None
            }.items()
        ]

    def check(self, model_type: str):
        """
        Raise ValueError if model_type does not match the filter expected model_type.
        """
        if self.model_type != model_type:
            raise ValueError(
                f"model_type {model_type!r} does not match filter.model_type {self.model_type!r}"
            )


class BaseParams(BaseModel):
    model_type: str

    def check(self, model_type: str):
        """
        Raise ValueError if model_type does not match the params' expected model_type.
        """
        if self.model_type != model_type:
            raise ValueError(
                f"model_type {model_type!r} does not match params.model_type {self.model_type!r}"
            )


class Macro(BaseModel):
    name: str = Field(description="Name of the macro")
    value: str | None = Field(None, description="Value of the macro")
    is_password: bool = Field(
        False, description="Indicates whether the macro value is a password or not"
    )
    description: str | None = Field(None, description="Macro description")
