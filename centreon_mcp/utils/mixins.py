from typing import Any, ClassVar, Self

from pydantic import BaseModel

from centreon_mcp.utils.request import request


class CreateMixin[Params: BaseModel]:
    """
    Mixin to add to a Centreon Model a creation method via heritage
    """

    endpoint: ClassVar[str]

    @classmethod
    async def create(cls, params: Params) -> bool:
        """
        Create a resource using the model's endpoint.
        Return True if successful; otherwise, raise an exception.
        """
        payload = params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
        await request("POST", cls.endpoint, payload)
        return True


class ReadMixin:
    """
    Mixin to add to a Centreon Model a get method via heritage
    """

    endpoint: ClassVar[str]

    @classmethod
    async def get(cls: type[Self], model_id: int) -> Self:
        """
        Get a centreon model using the model's endpoint.
        """
        content = await request("GET", f"{cls.endpoint}/{model_id}")
        return cls(**content)


class DeleteMixin:
    """
    Mixin to add to a Centreon Model a delete method via heritage
    """

    endpoint: ClassVar[str]

    @classmethod
    async def delete(cls, model_id: int) -> bool:
        """
        Delete a resource using the model's endpoint.
        Return True if successful; otherwise, raise an exception.
        """
        await request("DELETE", f"{cls.endpoint}/{model_id}")
        return True


class UpdateMixin[Params: BaseModel](ReadMixin):
    """
    Mixin to add to a Centreon Model a update method via heritage
    """

    endpoint: ClassVar[str]
    full_params_cls: ClassVar[type[BaseModel]]

    @classmethod
    async def update(cls, model_id: int, params: Params) -> bool:
        """
        Update a reource using the model's endpoint.
        Return True if successful; otherwise, raise an exception.
        """
        payload = params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
        await request("PUT", f"{cls.endpoint}/{model_id}", payload)
        return True


class PatchMixin[Params: BaseModel]:
    """
    Mixin to add to a Centreon Model a patch method via heritage
    """

    endpoint: ClassVar[str]

    @classmethod
    async def patch(cls, host_id: int, params: Params) -> bool:
        """
        Patch a resource using the model's endpoint.
        Return True if successful; otherwise, raise an exception.
        """
        payload = params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
        await request("PATCH", f"{cls.endpoint}/{host_id}", payload)
        return True


class ListMixin:
    """
    Mixin to add to a Centreon Model a list method via heritage
    """

    endpoint: ClassVar[str]

    @classmethod
    async def list(
        cls: type[Self],
        search: str | None = None,
        limit: int | None = None,
        page: int | None = None,
        sort_by: str | None = None,
        extras: dict[str, Any] | None = None,
    ) -> list[Self]:
        """
        List resources matching the search string using the model's endpoint.
        """
        extras = extras or {}
        params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by, **extras}
        content = await request("GET", cls.endpoint, params=params)
        return [cls(**item) for item in content["result"]]
