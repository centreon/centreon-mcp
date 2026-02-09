import asyncio
import json
from typing import ClassVar, Literal, Type

from pydantic import BaseModel

from centreon_mcp.utils.type import CentreonBaseModel


class BaseOrder(BaseModel):
    order: Literal["ASC", "DESC"] = "ASC"


class BaseFilter(BaseModel):
    links: ClassVar[dict[str, Type[CentreonBaseModel]]] = {}

    async def fill(self, field: str, cls: Type[CentreonBaseModel]) -> None:
        """
        Fill filter field id using field name and class.
        """
        name = getattr(self, f"{field}_name")
        if name is None:
            return
        conditions = {"$and": [{"name": {"$eq": name}}]}
        items = await cls.list(search=json.dumps(conditions))
        for item in items:
            if getattr(item, "name") == name:
                setattr(self, f"{field}_id", getattr(item, "id"))
                return
        raise ValueError(f"{cls.__name__} with name '{name}' not found.")

    async def complete(self) -> None:
        """
        Compute filters based on fields not available in Centreon API.
        """
        tasks = [
            asyncio.create_task(self.fill(field, cls))
            for field, cls in self.links.items()
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
