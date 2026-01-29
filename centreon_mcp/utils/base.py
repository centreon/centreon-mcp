from pydantic import BaseModel, Field

from centreon_mcp.utils.type import HostState


class BaseFilter(BaseModel):
    host_id: int | None = Field(None, serialization_alias="host.id")
    host_name: str | None = Field(None, serialization_alias="host.name")
    host_alias: str | None = Field(None, serialization_alias="host.alias")
    host_address: str | None = Field(None, serialization_alias="host.address")
    host_state: HostState | None = Field(None, serialization_alias="host.state")
    poller_id: int | None = Field(None, serialization_alias="poller.id")
    host_group_id: int | None = Field(None, serialization_alias="host_group.id")

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
