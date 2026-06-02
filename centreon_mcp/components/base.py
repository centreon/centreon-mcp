import asyncio
import json
from collections.abc import Sequence

from pydantic import BaseModel

from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, PatchMixin


async def _list[CentreonModel: ListMixin](
    model: type[CentreonModel],
    filters: Sequence[BaseFilter] | None = None,
    limit: int = 10,
    page: int = 1,
    order: BaseOrder | None = None,
) -> list[CentreonModel]:
    """
    Generic function to list resources based on provided filters, pagination and order.
    """
    search = json.dumps(BaseFilter.join(filters))
    sort_by = order.model_dump_json() if order else None
    return await model.list(search, limit, page, sort_by)


async def _delete[CentreonModel: DeleteMixin](
    model: type[CentreonModel], model_ids: list[int]
) -> dict[int, bool | BaseException]:
    """
    Generic function to delete multiple resources based on their ids.
    """
    tasks = [asyncio.create_task(model.delete(model_id)) for model_id in model_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return dict(zip(model_ids, results, strict=True))


async def _create[CentreonModel: CreateMixin](
    model: type[CentreonModel], params: BaseModel
) -> bool:
    """
    Generic function to create a resource based on params.
    """
    return await model.create(params)


async def _patch[CentreonModel: PatchMixin](
    model: type[CentreonModel], model_id: int, params: BaseModel
) -> bool:
    """
    Generic function to patch a resource based on params.
    """
    return await model.patch(model_id, params)
