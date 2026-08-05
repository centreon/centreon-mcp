import asyncio
import json
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, ClassVar, Self

from pydantic import BaseModel

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseParams, BaseResource
from centreon_mcp.utils.request import request


class BaseMixin:
    model_type: ClassVar[str]
    endpoint: ClassVar[str]


class CreateMixin[Params: BaseParams](BaseMixin):
    """
    Mixin to add to a Centreon Model a creation method via heritage
    """

    @classmethod
    async def create(cls, params: Params) -> bool:
        """
        Create a resource using the model's endpoint.
        Return True if successful; otherwise, raise an exception.
        """
        payload = params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
        await request("POST", cls.endpoint, payload)
        return True


class ReadMixin(BaseMixin):
    """
    Mixin to add to a Centreon Model a get method via heritage
    """

    @classmethod
    async def get(cls: type[Self], model_id: int) -> Self:
        """
        Get a centreon model using the model's endpoint.
        """
        content = await request("GET", f"{cls.endpoint}/{model_id}")
        return cls(**content)


class DeleteMixin(BaseMixin):
    """
    Mixin to add to a Centreon Model a delete method via heritage
    """

    @classmethod
    async def _delete(cls, model_id: int) -> bool:
        """
        Delete a resource using the model's endpoint.
        Return True if successful; otherwise, raise an exception.
        """
        await request("DELETE", f"{cls.endpoint}/{model_id}")
        return True

    @classmethod
    async def delete(cls, model_ids: list[int]) -> dict[int, bool | BaseException]:
        """
        Delete multiple resources concurrently by their ids.
        Return a dict mapping each id to True on success, or to the raised
        exception on failure; never raises for individual deletion errors.
        """
        tasks = [asyncio.create_task(cls._delete(model_id)) for model_id in model_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return dict(zip(model_ids, results, strict=True))


class UpdateMixin[PartialParams: BaseParams](BaseMixin, ABC):
    """
    Mixin to add to a Centreon Model a update method via heritage
    """

    @classmethod
    @abstractmethod
    async def update(cls, model_id: int, params: PartialParams) -> bool: ...


class PutMixin[PartialParams: BaseParams, FullParams: BaseParams](
    UpdateMixin[PartialParams], ReadMixin
):
    """
    Mixin to add to a Centreon Model a update method via heritage
    """

    full_params_cls: ClassVar[type[FullParams]]

    @classmethod
    async def put(cls, model_id: int, params: FullParams) -> bool:
        """
        Put a resource using the model's endpoint.
        Return True if successful; otherwise, raise an exception.
        """
        payload = params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
        await request("PUT", f"{cls.endpoint}/{model_id}", payload)
        return True

    @classmethod
    async def update(cls, model_id: int, params: PartialParams) -> bool:
        """
        Update a resource by fetching its current state, merging the partial params over it, and sending the result via PUT.
        Return True if successful; otherwise, raise an exception.
        """
        current = await cls.get(model_id)
        data = current.model_dump(exclude={"id"}, exclude_none=True)  # type: ignore
        data |= params.model_dump(exclude_none=True, exclude={"model_type"})
        return await cls.put(model_id, cls.full_params_cls(**data))


class PatchMixin[PartialParams: BaseParams](UpdateMixin[PartialParams]):
    """
    Mixin to add to a Centreon Model a patch method via heritage
    """

    @classmethod
    async def patch(cls, model_id: int, params: PartialParams) -> bool:
        """
        Patch a resource using the model's endpoint.
        Return True if successful; otherwise, raise an exception.
        """
        payload = params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
        await request("PATCH", f"{cls.endpoint}/{model_id}", payload)
        return True

    @classmethod
    async def update(cls, model_id: int, params: PartialParams) -> bool:
        """
        Update a resource using PATCH method.
        Return True if successful; otherwise, raise an exception.
        """
        return await cls.patch(model_id, params)


class ListMixin[Filter: BaseFilter, Order: BaseOrder](BaseMixin):
    """
    Mixin to add to a Centreon Model a list method via heritage
    """

    @classmethod
    async def list(
        cls: type[Self],
        filters: Sequence[Filter] | None = None,
        limit: int | None = None,
        page: int | None = None,
        order: Order | None = None,
        extras: dict[str, Any] | None = None,
    ) -> list[Self]:
        """
        List resources matching the provided filters, pagination and order using the model's endpoint.
        """
        extras = extras or {}
        search = json.dumps(BaseFilter.join(filters))
        sort_by = order.model_dump_json(exclude={"model_type"}) if order else None
        params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by, **extras}
        content = await request("GET", cls.endpoint, params=params)
        return [cls(**item) for item in content["result"]]


class SetMixin[
    Params: BaseModel,
](BaseMixin):
    """
    Mixin to add to a Centreon Model a set method via heritage
    """

    set_endpoint: ClassVar[str]

    @classmethod
    async def set(cls, params: Params, resources: list[BaseResource]) -> bool:
        """
        Set an action on resources using the model's endpoint.
        Return True if successful; otherwise, raise an exception.
        """
        payload = {
            cls.model_type: params.model_dump(
                mode="json", exclude_none=True, exclude={"model_type"}
            ),
            "resources": [resource.dump() for resource in resources],
        }
        await request("POST", cls.set_endpoint, payload)
        return True


class CountMixin[Filter: BaseFilter](BaseMixin):
    """
    Mixin to add to a Centreon Model a count method via heritage
    """

    @classmethod
    async def count(cls: type[Self], filters: Sequence[Filter] | None = None) -> Self:
        """
        Count resources by status matching the provided filters using the model's endpoint.
        """
        params = {"search": json.dumps(BaseFilter.join(filters))}
        content = await request("GET", cls.endpoint, params=params)
        return cls(**content)
