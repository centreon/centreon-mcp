from collections.abc import Sequence
from enum import IntEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ResourceType = Literal["host", "service"]
StatusType = Literal["soft", "hard"]
HostStatus = Literal["UP", "DOWN", "UNREACHABLE", "PENDING"]
ServiceStatus = Literal["OK", "WARNING", "CRITICAL", "UNKNOWN", "PENDING"]
ResourceStatus = HostStatus | ServiceStatus

# Centreon search operators that match their value as an SQL LIKE pattern, with the hint appended
# to the description of every filter field using them.
LIKE_OPERATORS = {
    "$lk": "LIKE pattern: exact match unless it contains `%` (see the `filters` description).",
    "$nk": (
        "NOT LIKE pattern: excludes exact matches unless it contains `%` "
        "(see the `filters` description)."
    ),
}

# Description of the `filters` parameter of every tool taking a list of `BaseFilter`.
FILTERS_FIELD = Field(
    description=(
        "Filters to narrow down the results. Several filters are combined with OR; the fields set "
        "in one filter are combined with AND. Fields described as LIKE patterns use SQL LIKE "
        "matching: without wildcards the match is exact ('srv-01' matches only 'srv-01'); add `%` "
        "to match any sequence of characters: 'srv-%' (starts with), '%-01' (ends with), '%web%' "
        "(contains)."
    ),
)


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
    # Reject unknown fields: an ignored, misspelled field would silently widen the search.
    model_config = ConfigDict(extra="forbid")

    model_type: str

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        """
        Append the LIKE pattern hint to the description of every `$lk`/`$nk` field.
        """
        super().__pydantic_init_subclass__(**kwargs)
        changed = False
        for field in cls.model_fields.values():
            alias = field.serialization_alias
            hint = LIKE_OPERATORS.get(alias.split()[-1]) if alias else None
            if hint and hint not in (field.description or ""):
                field.description = f"{field.description} {hint}" if field.description else hint
                changed = True
        if changed:
            cls.model_rebuild(force=True)

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


class PageMetadata(BaseModel):
    """
    Paging information of a list result, built from the `meta` object of a Centreon API response.
    """

    page: int = Field(ge=1, description="Number of the returned page, starting at 1")
    limit: int = Field(ge=1, description="Maximum number of items returned per page")
    total: int = Field(
        ge=0,
        description=(
            "Total number of items matching the filters across all pages, not only this page. "
            "More pages remain while page * limit < total."
        ),
    )


class Page[T](BaseModel):
    """
    One page of a list result: the items of the requested page and the paging information
    needed to fetch the remaining ones.
    """

    results: list[T] = Field(
        description="Items of the requested page only, at most meta.limit of them"
    )
    meta: PageMetadata = Field(
        description=(
            "Paging information. When meta.page * meta.limit < meta.total, more items exist: "
            "call the tool again with page set to meta.page + 1 to get them."
        )
    )
