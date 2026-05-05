from typing import Any, ClassVar, Literal, TypeVar

from pydantic import BaseModel, Field, model_validator

from centreon_mcp.utils.request import request

T = TypeVar("T", bound="CentreonBaseModel")

ResourceType = Literal["host", "service"]

StatusType = Literal["soft", "hard"]


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


class CentreonBaseModel(BaseModel):
    endpoint: ClassVar[str]

    @classmethod
    async def list(
        cls: type[T],
        search: str | None = None,
        limit: int | None = None,
        page: int | None = None,
        sort_by: str | None = None,
    ) -> list[T]:
        """
        List resource of type T in real-time monitoring matching the search string.
        """
        params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by}
        content = await request("GET", cls.endpoint, params=params)
        return [cls(**item) for item in content["result"]]
