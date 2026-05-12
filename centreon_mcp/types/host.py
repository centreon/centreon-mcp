from enum import IntEnum
from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.types.base import CentreonBaseModel, StatusCount
from centreon_mcp.utils.request import request

HostStatus = Literal["UP", "DOWN", "UNREACHABLE", "PENDING"]


class Status(IntEnum):
    STATUS_DISABLED = 0
    STATUS_ENABLED = 1
    STATUS_DEFAULT = 2


class MonitoringServer(BaseModel):
    id: int
    name: str


class HostCategory(BaseModel):
    id: int
    name: str


class HostGroup(BaseModel):
    id: int
    name: str


class HostState(IntEnum):
    UP = 0
    DOWN = 1
    UNREACHABLE = 2
    PENDING = 4


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


class HostConfigurationParams(BaseModel):
    monitoring_server_id: int = Field(description="ID of the host's monitoring server")
    name: str = Field(description="Host name")
    address: str = Field(description="IP or domain of the host")
    alias: str | None = Field(default=None, description="Host alias")
    snmp_community: str | None = Field(default=None, description="Community of the SNMP agent")
    snmp_version: Literal["1", "2c", "3"] | None = Field(
        default=None, description="Version of the SNMP agent."
    )
    geo_coords: str | None = Field(default=None, description="Geographic coordinates of the host")
    severity_id: int | None = Field(default=None, description="Host severity ID of the host")
    check_command_id: int | None = Field(
        default=None, description="Check command ID. Must be of type 'Check'."
    )
    check_command_args: list[str] = Field(
        default_factory=list, description="Check command arguments"
    )
    max_check_attempts: int | None = Field(
        default=None,
        description="Define the number of times that the monitoring engine will retry the host check command if it returns any non-OK state",
    )
    normal_check_interval: int | None = Field(
        default=None,
        description=(
            "Define the number of 'time units' between regularly scheduled checks of the host."
            "With the default time unit of 60s, this number will mean multiples of 1 minute."
        ),
    )
    retry_check_interval: int | None = Field(
        default=None,
        description=(
            "Define the number of 'time units' to wait before scheduling a re-check for this host after a non-UP state was detected."
            "With the default time unit of 60s, this number will mean multiples of 1 minute."
            "Once the host has been retried max_check_attempts times without a change in its status, it will revert to being scheduled at its 'normal' check interval rate."
        ),
    )
    active_check_enabled: Status | None = Field(
        default=None, description="Indicates whether active checks are enabled or not"
    )
    passive_check_enabled: Status | None = Field(
        default=None, description="Indicates whether passive checks are enabled or not"
    )
    notification_enabled: Status | None = Field(
        default=None, description="Specify whether notifications for this host are enabled or not"
    )
    add_inherited_contact_group: bool | None = Field(
        default=None,
        description=(
            "Only used when notification inheritance for hosts and services is set to vertical inheritance only."
            "When enabled, the contactgroup definition will not override the definitions on template levels, it will be appended instead."
        ),
    )
    add_inherited_contact: bool | None = Field(
        default=None,
        description=(
            "Only used when notification inheritance for hosts and services is set to vertical inheritance only."
            "When enabled, the contact definition will not override the definitions on template levels, it will be appended instead."
        ),
    )
    first_notification_delay: int | None = Field(
        default=None,
        description=(
            "Define the number of 'time units' to wait before sending out the first alert notification when this host enters a non-UP state."
            "With the default time unit of 60s, this number will mean multiples of 1 minute."
        ),
    )
    recovery_notification_delay: int | None = Field(
        default=None,
        description=(
            "Define the number of 'time units' to wait before sending out the recovery notification when this host enters an UP state."
            "With the default time unit of 60s, this number will mean multiples of 1 minute."
        ),
    )
    acknowledgement_timeout: int | None = Field(
        default=None, description="Specify a duration of acknowledgement for this host."
    )
    freshness_checked: Status | None = Field(
        default=None, description="Indicates whether freshness is checked or not"
    )
    freshness_threshold: int | None = Field(
        default=None, description="Specify the freshness threshold (in seconds) for this host."
    )
    flap_detection_enabled: Status | None = Field(
        default=None, description="Indicates whether the flap detection is enabled or not"
    )
    low_flap_threshold: int | None = Field(
        ge=0,
        le=100,
        default=None,
        description="Specify the low state change threshold used in flap detection for this host",
    )
    high_flap_threshold: int | None = Field(
        ge=0,
        le=100,
        default=None,
        description="Specify the high state change threshold used in flap detection for this host",
    )
    event_handler_command_id: int | None = Field(
        default=None, description="Event handler command ID"
    )
    event_handler_command_args: list[str] = Field(
        default_factory=list, description="Event handler command arguments"
    )
    comment: str | None = Field(default=None, description="Comment for this host")
    is_activated: bool | None = Field(
        default=None, description="Indicates whether the host template is activated or not"
    )
    categories: list[int] | None = Field(
        default=None,
        description="Define the host category IDs that should be associated with this host",
    )
    groups: list[int] | None = Field(
        default=None,
        description="Define the host groups IDs that should be associated with this host",
    )


class HostConfiguration(CentreonBaseModel):
    endpoint: ClassVar[str] = "configuration/hosts"

    id: int
    name: str
    alias: str
    address: str
    monitoring_server: MonitoringServer
    normal_check_interval: int | None
    retry_check_interval: int | None
    categories: list[HostCategory]
    groups: list[HostGroup]
    is_activated: bool

    @classmethod
    async def create(cls, params: HostConfigurationParams) -> None:
        """
        Create a host configuration.
        """
        payload = params.model_dump(mode="json")
        await request("POST", cls.endpoint, payload)

    @classmethod
    async def update(cls, host_id: int, params: HostConfigurationParams) -> None:
        """
        Partially update a host configuration.
        """
        payload = params.model_dump(mode="json")
        await request("PATCH", f"{cls.endpoint}/{host_id}", payload)

    @classmethod
    async def delete(cls, host_id: int) -> None:
        """
        Delete a host configuration.
        """
        await request("DELETE", f"{cls.endpoint}/{host_id}")
