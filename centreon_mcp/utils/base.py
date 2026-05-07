import json
from collections.abc import Sequence
from typing import Literal

from pydantic import BaseModel

from centreon_mcp.utils.type import CentreonBaseModel


class BaseOrder(BaseModel):
    order: Literal["ASC", "DESC"] = "ASC"


class BaseFilter(BaseModel):
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
                for condition, value in self.model_dump(mode="json", by_alias=True).items()
                if value is not None
            }.items()
        ]


async def _list[CentreonModelType: CentreonBaseModel, OrderType: BaseOrder, FilterType: BaseFilter](
    model: type[CentreonModelType],
    order_cls: type[OrderType],
    filters: list[FilterType] | None = None,
    limit: int = 10,
    page: int = 1,
    order: OrderType | None = None,
) -> list[CentreonModelType]:
    """
    Generic function to list ressources in real-time monitoring based on provided filters, pagination and order
    """
    order = order or order_cls()
    search = json.dumps(BaseFilter.join(filters))
    sort_by = order.model_dump_json()
    return await model.list(search, limit, page, sort_by)
