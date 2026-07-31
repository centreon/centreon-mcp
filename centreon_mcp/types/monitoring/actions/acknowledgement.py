from datetime import datetime
from typing import ClassVar, Literal

from pydantic import BaseModel

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseParams, BaseResource
from centreon_mcp.utils.mixins import DeleteMixin, ListMixin, ReadMixin, SetMixin
from centreon_mcp.utils.request import request


class AcknowledgementOrder(BaseOrder):
    model_type: Literal["acknowledgement"] = "acknowledgement"

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
    model_type: Literal["acknowledgement"] = "acknowledgement"

    # Fields available for filtering in Centreon API


class AcknowledgementParams(BaseParams):
    model_type: Literal["acknowledgement"] = "acknowledgement"

    comment: str
    with_services: bool = True
    is_notify_contacts: bool = True
    is_persistent_comment: bool = True
    is_sticky: bool = True
    force_active_checks: bool = True


class Acknowledgement(
    BaseModel,
    ReadMixin,
    DeleteMixin,
    ListMixin[AcknowledgementFilter, AcknowledgementOrder],
    SetMixin[AcknowledgementParams],
):
    endpoint: ClassVar[str] = "monitoring/acknowledgements"
    set_endpoint: ClassVar[str] = "monitoring/resources/acknowledge"
    model_type: ClassVar[str] = "acknowledgement"

    id: int
    host_id: int
    service_id: int | None = None
    author_id: int
    author_name: str
    comment: str
    deletion_time: datetime | None = None
    entry_time: datetime | None = None
    is_notify_contacts: bool = True
    is_persistent_comment: bool = True
    is_sticky: bool = True

    @classmethod
    async def _delete(cls, model_id: int) -> bool:
        """
        Delete (disacknowledge) an acknowledgement by id.

        No "monitoring/acknowledgements/{id}" delete endpoint exists, so the
        acknowledgement is fetched first to build the resource payload
        expected by "monitoring/resources/acknowledgements". This mirrors
        the other actions' delete behavior, allowing them to share the same
        cancellation tools.

        Return True if successful; otherwise, raise an exception.
        """
        acknowledgement = await cls.get(model_id)
        resource = BaseResource(
            type="service" if acknowledgement.service_id else "host",
            resource_id=acknowledgement.service_id or acknowledgement.host_id,
            host_id=acknowledgement.host_id,
        )
        payload = {
            "disacknowledgement": {"with_services": False},
            "resources": [resource.dump()],
        }
        await request("DELETE", "monitoring/resources/acknowledgements", payload=payload)
        return True
