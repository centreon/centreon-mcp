import json
from typing import Literal, Sequence, Type, TypeVar

from pydantic import BaseModel

from centreon_mcp.utils.type import T

OrderType = TypeVar("OrderType", bound="BaseOrder")
FilterType = TypeVar("FilterType", bound="BaseFilter")


class BaseOrder(BaseModel):
    order: Literal["ASC", "DESC"] = "ASC"


class BaseFilter(BaseModel):
    @staticmethod
    def join(filters: Sequence["BaseFilter"] | None) -> dict:
        """
        Join multiple filters conditions using OR operaror.
        """
        return (
            {
                "$or": [
                    {"$and": filter.conditions}
                    for filter in filters
                    if filter.conditions
                ]
            }
            if filters
            else {}
        )

    @property
    def conditions(self) -> list:
        """
        Generate list of conditions dictionary for filtering.
        """
        return [
            {name: {operator: value}}
            for (name, operator), value in {
                tuple(condition.split()): value
                for condition, value in self.model_dump(by_alias=True).items()
                if value is not None
            }.items()
        ]


async def _list(
    model: Type[T],
    order_cls: Type[OrderType],
    filters: list[FilterType] | None = None,
    limit: int = 10,
    page: int = 1,
    order: OrderType | None = None,
) -> list[T]:
    """
    Generic function to list ressources in real-time monitoring based on provided filters, pagination and order
    """
    order = order or order_cls()
    search = json.dumps(BaseFilter.join(filters))
    sort_by = order.model_dump_json()
    return await model.list(search, limit, page, sort_by)
