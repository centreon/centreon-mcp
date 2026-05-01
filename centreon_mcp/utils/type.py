from datetime import UTC, datetime
from enum import IntEnum
from typing import Any, ClassVar, Literal, TypeVar

from pydantic import BaseModel, Field, model_validator

from centreon_mcp.utils.request import request

T = TypeVar("T", bound="CentreonBaseModel")

ResourceType = Literal["host", "service"]
StatusType = Literal["hard", "soft"]
HostStatus = Literal["UP", "DOWN", "UNREACHABLE", "PENDING"]
ServiceStatus = Literal["OK", "WARNING", "CRITICAL", "UNKNOWN", "PENDING"]
ResourceStatus = HostStatus | ServiceStatus


class HostState(IntEnum):
    UP = 0
    DOWN = 1
    UNREACHABLE = 2
    PENDING = 4


class ServiceState(IntEnum):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3
    PENDING = 4


class CentreonBaseModel(BaseModel):
    endpoint: ClassVar[str]

    @classmethod
    async def list(
        cls: type[T],
        search: str | None = None,
        limit: int | None = None,
        page: int | None = None,
        sort_by: str | None = None,
    ) -> list[T]:
        """
        List resource of type T in real-time monitoring matching the search string.
        """
        params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by}
        content = await request("GET", cls.endpoint, params=params)
        return [cls(**item) for item in content["result"]]


class Status(BaseModel):
    code: int
    name: ResourceStatus
    severity_code: int


class Resource(BaseModel):
    endpoint: ClassVar[str] = "monitoring/resources"

    uuid: str
    id: int
    type: ResourceType
    name: str
    alias: str | None
    fqdn: str | None
    host_id: int
    service_id: int | None
    monitoring_server_name: str
    is_in_downtime: bool
    is_acknowledged: bool
    is_in_flapping: bool
    status: Status
    information: str | None
    has_active_checks_enabled: bool
    has_passive_checks_enabled: bool
    last_status_change: datetime | None
    last_check: str | None
    tries: str | None

    @classmethod
    async def list(
        cls,
        search: str,
        types: str,
        statuses: str | None = None,
        hostgroup_names: str | None = None,
        servicegroup_names: str | None = None,
        host_category_names: str | None = None,
        service_category_names: str | None = None,
        monitoring_server_names: str | None = None,
        status_types: str | None = None,
        limit: int | None = None,
        page: int | None = None,
        sort_by: str | None = None,
    ) -> list["Resource"]:
        """
        List ressources (hosts and services) in real-time monitoring.
        """
        params = {
            "search": search,
            "limit": limit,
            "page": page,
            "sort_by": sort_by,
            "types": types,
            "statuses": statuses,
            "hostgroup_names": hostgroup_names,
            "servicegroup_names": servicegroup_names,
            "host_category_names": host_category_names,
            "service_category_names": service_category_names,
            "monitoring_server_names": monitoring_server_names,
            "status_types": status_types,
        }
        content = await request("GET", cls.endpoint, params=params)
        return [cls(**item) for item in content["result"]]


class StatusCount(BaseModel):
    pending: int
    total: int

    @model_validator(mode="before")
    @classmethod
    def flatten(cls, data: dict[str, Any]):
        return {
            "total": data.pop("total"),
            **{status: count["total"] for status, count in data.items()},
        }


class HostStatusCount(StatusCount):
    up: int
    down: int
    unreachable: int


class Host(BaseModel):
    @staticmethod
    async def count_by_status(search: str | None) -> HostStatusCount:
        """
        Count hosts by status.
        """
        params = {"search": search}
        content = await request("GET", "monitoring/hosts/status", params=params)
        return HostStatusCount(**content)


class ServiceStatusCount(StatusCount):
    critical: int
    unknown: int
    ok: int
    warning: int


class Service(BaseModel):
    @staticmethod
    async def count_by_status(search: str | None) -> ServiceStatusCount:
        """
        Count services by status.
        """
        params = {"search": search}
        content = await request("GET", "monitoring/services/status", params=params)
        return ServiceStatusCount(**content)


class HostGroup(CentreonBaseModel):
    endpoint: ClassVar[str] = "monitoring/hostgroups"

    id: int
    name: str


class ServiceGroup(CentreonBaseModel):
    endpoint: ClassVar[str] = "monitoring/servicegroups"

    id: int
    name: str


class MonitoringServer(CentreonBaseModel):
    endpoint: ClassVar[str] = "monitoring/servers"

    id: int
    name: str
    address: str | None
    description: str | None = None
    is_running: bool
    last_alive: int | None
    version: str | None


class BaseResource(BaseModel):
    type: ResourceType
    resource_id: int = Field(..., serialization_alias="id")
    host_id: int

    def dump(self) -> dict[str, Any]:
        """
        Dump the resource to a dict with the expected format for the API.
        """
        return {
            "parent": {"id": self.host_id},
            **self.model_dump(mode="json", by_alias=True, exclude={"host_id"}),
        }


class AcknowledgementParams(BaseModel):
    comment: str
    with_services: bool = True
    is_notify_contacts: bool = True
    is_persistent_comment: bool = True
    is_sticky: bool = True
    force_active_checks: bool = True


class AcknowledgementResource(BaseResource):
    pass


class Acknowledgement(CentreonBaseModel):
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
    async def add(params: AcknowledgementParams, resources: list[AcknowledgementResource]) -> None:
        """
        Add an acknowledgement on multiple resources.
        """
        payload = {
            "acknowledgement": params.model_dump(mode="json"),
            "resources": [resource.dump() for resource in resources],
        }
        await request("POST", "monitoring/resources/acknowledge", payload=payload)

    @staticmethod
    async def cancel(with_services: bool, resources: list[AcknowledgementResource]) -> None:
        """
        Cancel acknowledgements on multiple resources.
        """
        payload = {
            "disacknowledgement": {"with_services": with_services},
            "resources": [resource.dump() for resource in resources],
        }
        await request("DELETE", "monitoring/resources/acknowledgements", payload=payload)


class CheckResource(BaseResource):
    pass


class Check(BaseModel):
    @staticmethod
    async def submit(is_forced: bool, resources: list[CheckResource]) -> None:
        """
        Submit a check request on multiple resources (hosts and services).
        When `is_forced` is True, the check is executed immediately regardless of
        the configured check interval. Otherwise, the check is scheduled for the
        next available execution slot.
        """
        payload = {
            "check": {"is_forced": is_forced},
            "resources": [resource.dump() for resource in resources],
        }
        await request("POST", "monitoring/resources/check", payload=payload)


class DowntimeParams(BaseModel):
    start_time: datetime
    end_time: datetime
    is_fixed: bool
    duration: int
    comment: str
    with_services: bool


class DowntimeResource(BaseResource):
    pass


class Downtime(CentreonBaseModel):
    endpoint: ClassVar[str] = "monitoring/downtimes"

    id: int
    author_id: int
    author_name: str
    host_id: int
    service_id: int | None
    poller_id: int
    comment: str
    duration: int | None
    entry_time: datetime | None
    start_time: datetime | None
    end_time: datetime | None
    deletion_time: datetime | None
    actual_start_time: datetime | None
    actual_end_time: datetime | None
    is_started: bool
    is_fixed: bool
    is_cancelled: bool

    @classmethod
    async def set(cls, params: DowntimeParams, resources: list[DowntimeResource]) -> None:
        """
        Set a downtime on multiple resources.
        """
        payload = {
            "downtime": params.model_dump(mode="json"),
            "resources": [resource.dump() for resource in resources],
        }
        await request("POST", "monitoring/resources/downtime", payload=payload)

    @staticmethod
    async def cancel(downtime_id: int) -> None:
        """
        Cancel a downtime.
        """
        await request("DELETE", f"monitoring/downtimes/{downtime_id}")


class CommentResource(BaseResource):
    comment: str
    date: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))


class Comment(CentreonBaseModel):
    @staticmethod
    async def add(resources: list[CommentResource]) -> None:
        """
        Add comments on multiple resources.
        """
        payload = {"resources": [resource.dump() for resource in resources]}
        await request("POST", "monitoring/resources/comments", payload=payload)


class CommandType(IntEnum):
    NOTIFICATION = 1
    CHECK = 2
    MISCELLANEOUS = 3
    DISCOVERY = 4


class CommandArgument(BaseModel):
    name: str
    description: str


class CommandMacroType(IntEnum):
    HOST = 1
    SERVICE = 2


class CommandMacro(BaseModel):
    name: str
    type: CommandMacroType
    description: str


class CommandParams(BaseModel):
    name: str
    type: CommandType
    command_line: str
    is_shell: bool = Field(
        default=False,
        description=(
            "Is required if your command requires shell features like pipes, redirections, globbing etc."
            "If you are using the monitoring engine this option cannot be disabled."
            "Note that commands that require shell features are slowing down the poller server."
        ),
    )
    argument_example: str | None = Field(
        default=None, description="Example of command argument values"
    )
    arguments: list[CommandArgument] = Field(
        default_factory=list,
        description="descriptions of arguments used in the command line",
    )
    macros: list[CommandMacro] = Field(
        default_factory=list,
        description="descriptions of macros used in the command line",
    )
    connector_id: int | None = Field(
        default=None,
        description="A connector is run in the background and executes specific commands without the need to execute a binary.",
    )
    graph_template_id: int | None = Field(
        default=None, description="Graph template for the command"
    )


class Command(CentreonBaseModel):
    endpoint: ClassVar[str] = "configuration/commands"

    id: int
    name: str
    type: CommandType
    command_line: str
    is_activated: bool
    is_shell: bool
    is_locked: bool

    @staticmethod
    async def add(params: CommandParams) -> None:
        """
        Add a command.
        """
        payload = params.model_dump(mode="json")
        await request("POST", "configuration/commands", payload=payload)
