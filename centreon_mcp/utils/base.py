import asyncio
import json
from typing import ClassVar, Literal, Type, TypeVar

from pydantic import BaseModel

from centreon_mcp.utils.type import CentreonBaseModel, T

O = TypeVar("O", bound="BaseOrder")
F = TypeVar("F", bound="BaseFilter")


class ConstraintLink(BaseModel):
    cls: Type[CentreonBaseModel]
    object: str
    fields: list[str]


class BaseOrder(BaseModel):
    order: Literal["ASC", "DESC"] = "ASC"


class BaseFilter(BaseModel):
    links: ClassVar[list[ConstraintLink]] = []

    async def fill(self, link: ConstraintLink) -> None:
        """
        Fill filter field id using field name and class.
        """
        # If the objet id is already set, do nothing.
        if getattr(self, f"{link.object}_id", None) is not None:
            return

        # Generate conditions for searching the item based on provided fields.
        conditions: list[dict] = []
        for field in link.fields:
            value = getattr(self, f"{link.object}_{field}")
            if value is not None:
                conditions.append({field: {"$eq": value}})

        # If no conditions are generated, objet don't matter in the filter.
        if len(conditions) == 0:
            return

        # Else, search for the objet id using conditions
        items = await link.cls.list(search=json.dumps({"$and": conditions}))

        # If no item is found, raise an error with the conditions used for searching.
        if len(items) == 0:
            msg = f"{link.cls.__name__} with with conditions {conditions} not found."
            raise ValueError(msg)

        # Else, set the objet id attribute with the found item's id.
        setattr(self, f"{link.object}_id", getattr(items[0], "id"))

    async def complete(self) -> None:
        """
        Compute filters based on fields not available in Centreon API.
        """
        tasks = [asyncio.create_task(self.fill(link)) for link in self.links]
        await asyncio.gather(*tasks)

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
    order_cls: Type[O],
    filters: list[F] | None = None,
    limit: int = 10,
    page: int = 1,
    order: O | None = None,
) -> list[T]:
    """
    Generic function to list ressources in real-time monitoring based on provided filters, pagination and order
    """
    filters = filters or []
    order = order or order_cls()
    await asyncio.gather(*(filter.complete() for filter in filters))
    conditions = (
        {
            "$or": [
                {"$and": filter.conditions} for filter in filters if filter.conditions
            ]
        }
        if filters
        else {}
    )
    search = json.dumps(conditions)
    sort_by = order.model_dump_json()
    return await model.list(search, limit, page, sort_by)
