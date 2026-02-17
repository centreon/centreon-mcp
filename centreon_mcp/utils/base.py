import asyncio
import json
from typing import ClassVar, Literal, Type

from pydantic import BaseModel

from centreon_mcp.utils.type import CentreonBaseModel


class BaseOrder(BaseModel):
    order: Literal["ASC", "DESC"] = "ASC"


class BaseFilter(BaseModel):
    links: ClassVar[list[tuple[Type[CentreonBaseModel], str, list[str]]]] = []

    async def fill(
        self, cls: Type[CentreonBaseModel], objet: str, fields: list[str]
    ) -> None:
        """
        Fill filter field id using field name and class.
        """
        # If the objet id is already set, do nothing.
        if getattr(self, f"{objet}_id", None) is not None:
            return

        # Generate conditions for searching the item based on provided fields.
        conditions: list[dict] = []
        for field in fields:
            value = getattr(self, f"{objet}_{field}")
            if value is not None:
                conditions.append({field: {"$eq": value}})

        # If no conditions are generated, objet don't matter in the filter.
        if len(conditions) == 0:
            return

        # Else, search for the objet id using conditions
        items = await cls.list(search=json.dumps({"$and": conditions}))

        # If no item is found, raise an error with the conditions used for searching.
        if len(items) == 0:
            msg = f"{cls.__name__} with with conditions {conditions} not found."
            raise ValueError(msg)

        # Else, set the objet id attribute with the found item's id.
        setattr(self, f"{objet}_id", getattr(items[0], "id"))

    async def complete(self) -> None:
        """
        Compute filters based on fields not available in Centreon API.
        """
        tasks = [
            asyncio.create_task(self.fill(cls, object, fields))
            for cls, object, fields in self.links
        ]
        await asyncio.gather(*tasks)

    @property
    def conditions(self) -> list:
        """
        Generate list of conditions dictionary for filtering.
        """
        return [
            {name: {"$eq": value}}
            for name, value in self.model_dump(by_alias=True).items()
            if value is not None
        ]
