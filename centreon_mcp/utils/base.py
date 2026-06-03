from collections.abc import Sequence
from typing import Literal

from pydantic import BaseModel


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
