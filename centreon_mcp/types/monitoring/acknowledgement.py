from datetime import datetime
from typing import ClassVar, Literal

from pydantic import BaseModel

from centreon_mcp.types.base import BaseResource
from centreon_mcp.utils.base import BaseFilter, BaseOrder
from centreon_mcp.utils.mixins import ListMixin
from centreon_mcp.utils.request import request


class AcknowledgementOrder(BaseOrder):
    field: Literal[
        "id",
        "host.id",
        "host.name",
        "host.alias",
        "host.address",
        "host.state",
        "start_time",
        "end_time",
        "entry_time",
        "deletion_time",
    ] = "id"


class AcknowledgementFilter(BaseFilter):
    # Fields available for filtering in Centreon API
    pass


class AcknowledgementParams(BaseModel):
    comment: str
    with_services: bool = True
    is_notify_contacts: bool = True
    is_persistent_comment: bool = True
    is_sticky: bool = True
    force_active_checks: bool = True


class AcknowledgementResource(BaseResource):
    pass


class Acknowledgement(BaseModel, ListMixin):
    endpoint: ClassVar[str] = "monitoring/acknowledgements"

    id: int
    host_id: int
    service_id: int | None
    author_id: int
    author_name: str
    comment: str
    deletion_time: datetime | None
    entry_time: datetime | None
    is_notify_contacts: bool
    is_persistent_comment: bool
    is_sticky: bool
    type: int

    @staticmethod
    async def add(params: AcknowledgementParams, resources: list[AcknowledgementResource]) -> bool:
        """
        Add an acknowledgement on multiple resources.
        Return True if successful; otherwise, raise an exception.
        """
        payload = {
            "acknowledgement": params.model_dump(mode="json"),
            "resources": [resource.dump() for resource in resources],
        }
        await request("POST", "monitoring/resources/acknowledge", payload=payload)
        return True

    @staticmethod
    async def cancel(with_services: bool, resources: list[AcknowledgementResource]) -> bool:
        """
        Cancel acknowledgements on multiple resources.
        Return True if successful; otherwise, raise an exception.
        """
        payload = {
            "disacknowledgement": {"with_services": with_services},
            "resources": [resource.dump() for resource in resources],
        }
        await request("DELETE", "monitoring/resources/acknowledgements", payload=payload)
        return True
