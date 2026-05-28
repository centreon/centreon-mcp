from enum import IntEnum
from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.types.base import EnablementStatus, StatusCount
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, PatchMixin, ReadMixin
from centreon_mcp.utils.request import request

DESCRIPTION = {
    "monitoring_server_id": "ID of the host's monitoring server",
    "name": "Host name",
    "address": "IP or domain of the host",
    "alias": "Host alias",
    "snmp_community": "Community of the SNMP agent",
    "snmp_version": "Version of the SNMP agent.",
    "geo_coords": "Geographic coordinates of the host",
    "severity_id": "Host severity ID of the host",
    "check_command_id": "Check command ID. Must be of type 'Check'.",
    "check_command_args": "Check command arguments",
    "max_check_attempts": "Define the number of times that the monitoring engine will retry the host check command if it returns any non-OK state",
    "normal_check_interval": (
        "Define the number of 'time units' between regularly scheduled checks of the host."
        "With the default time unit of 60s, this number will mean multiples of 1 minute."
    ),
    "retry_check_interval": (
        "Define the number of 'time units' to wait before scheduling a re-check for this host after a non-UP state was detected."
        "With the default time unit of 60s, this number will mean multiples of 1 minute."
        "Once the host has been retried max_check_attempts times without a change in its status, it will revert to being scheduled at its 'normal' check interval rate."
    ),
    "active_check_enabled": "Indicates whether active checks are enabled or not",
    "passive_check_enabled": "Indicates whether passive checks are enabled or not",
    "notification_enabled": "Specify whether notifications for this host are enabled or not",
    "add_inherited_contact_group": (
        "Only used when notification inheritance for hosts and services is set to vertical inheritance only."
        "When enabled, the contactgroup definition will not override the definitions on template levels, it will be appended instead."
    ),
    "add_inherited_contact": (
        "Only used when notification inheritance for hosts and services is set to vertical inheritance only."
        "When enabled, the contact definition will not override the definitions on template levels, it will be appended instead."
    ),
    "first_notification_delay": (
        "Define the number of 'time units' to wait before sending out the first alert notification when this host enters a non-UP state."
        "With the default time unit of 60s, this number will mean multiples of 1 minute."
    ),
    "recovery_notification_delay": (
        "Define the number of 'time units' to wait before sending out the recovery notification when this host enters an UP state."
        "With the default time unit of 60s, this number will mean multiples of 1 minute."
    ),
    "acknowledgement_timeout": "Specify a duration of acknowledgement for this host.",
    "freshness_checked": "Indicates whether freshness is checked or not",
    "freshness_threshold": "Specify the freshness threshold (in seconds) for this host.",
    "flap_detection_enabled": "Indicates whether the flap detection is enabled or not",
    "low_flap_threshold": "Specify the low state change threshold used in flap detection for this host",
    "high_flap_threshold": "Specify the high state change threshold used in flap detection for this host",
    "event_handler_command_id": "Event handler command ID",
    "event_handler_command_args": "Event handler command arguments",
    "comment": "Comment for this host",
    "is_activated": "Indicates whether the host template is activated or not",
    "categories": "Define the host category IDs that should be associated with this host",
    "groups": "Define the host groups IDs that should be associated with this host",
}

HostStatus = Literal["UP", "DOWN", "UNREACHABLE", "PENDING"]


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


class HostConfigurationBaseParams(BaseModel):
    alias: str | None = Field(None, description=DESCRIPTION["alias"])
    snmp_community: str | None = Field(None, description=DESCRIPTION["snmp_community"])
    snmp_version: Literal["1", "2c", "3"] | None = Field(
        None, description=DESCRIPTION["snmp_version"]
    )
    geo_coords: str | None = Field(None, description=DESCRIPTION["geo_coords"])
    severity_id: int | None = Field(None, description=DESCRIPTION["severity_id"])
    check_command_id: int | None = Field(None, description=DESCRIPTION["check_command_id"])
    check_command_args: list[str] | None = Field(
        None, description=DESCRIPTION["check_command_args"]
    )
    max_check_attempts: int | None = Field(None, description=DESCRIPTION["max_check_attempts"])
    normal_check_interval: int | None = Field(
        None, description=DESCRIPTION["normal_check_interval"]
    )
    retry_check_interval: int | None = Field(None, description=DESCRIPTION["retry_check_interval"])
    active_check_enabled: EnablementStatus | None = Field(
        None, description=DESCRIPTION["active_check_enabled"]
    )
    passive_check_enabled: EnablementStatus | None = Field(
        None, description=DESCRIPTION["passive_check_enabled"]
    )
    notification_enabled: EnablementStatus | None = Field(
        None, description=DESCRIPTION["notification_enabled"]
    )
    add_inherited_contact_group: bool | None = Field(
        None, description=DESCRIPTION["add_inherited_contact_group"]
    )
    add_inherited_contact: bool | None = Field(
        None, description=DESCRIPTION["add_inherited_contact"]
    )
    first_notification_delay: int | None = Field(
        None, description=DESCRIPTION["first_notification_delay"]
    )
    recovery_notification_delay: int | None = Field(
        None, description=DESCRIPTION["recovery_notification_delay"]
    )
    acknowledgement_timeout: int | None = Field(
        None, description=DESCRIPTION["acknowledgement_timeout"]
    )
    freshness_checked: EnablementStatus | None = Field(
        None, description=DESCRIPTION["freshness_checked"]
    )
    freshness_threshold: int | None = Field(None, description=DESCRIPTION["freshness_threshold"])
    flap_detection_enabled: EnablementStatus | None = Field(
        None, description=DESCRIPTION["flap_detection_enabled"]
    )
    low_flap_threshold: int | None = Field(
        None, ge=0, le=100, description=DESCRIPTION["low_flap_threshold"]
    )
    high_flap_threshold: int | None = Field(
        None, ge=0, le=100, description=DESCRIPTION["high_flap_threshold"]
    )
    event_handler_command_id: int | None = Field(
        None, description=DESCRIPTION["event_handler_command_id"]
    )
    event_handler_command_args: list[str] | None = Field(
        None, description=DESCRIPTION["event_handler_command_args"]
    )
    comment: str | None = Field(None, description=DESCRIPTION["comment"])
    is_activated: bool | None = Field(None, description=DESCRIPTION["is_activated"])
    categories: list[int] | None = Field(None, description=DESCRIPTION["categories"])
    groups: list[int] | None = Field(None, description=DESCRIPTION["groups"])


class HostConfigurationFullParams(HostConfigurationBaseParams):
    monitoring_server_id: int = Field(description=DESCRIPTION["monitoring_server_id"])
    name: str = Field(description=DESCRIPTION["name"])
    address: str = Field(description=DESCRIPTION["address"])


class HostConfigurationPartialParams(HostConfigurationBaseParams):
    monitoring_server_id: int | None = Field(None, description=DESCRIPTION["monitoring_server_id"])
    name: str | None = Field(None, description=DESCRIPTION["name"])
    address: str | None = Field(None, description=DESCRIPTION["address"])


class HostConfiguration(
    BaseModel,
    CreateMixin[HostConfigurationFullParams],
    PatchMixin[HostConfigurationPartialParams],
    DeleteMixin,
    ReadMixin,
    ListMixin,
):
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
