from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseParams, EnablementStatus
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, PatchMixin

DESCRIPTION = {
    "name": "Host template name",
    "alias": "Host template alias",
    "snmp_community": "Community of the SNMP agent",
    "snmp_version": "Version of the SNMP agent.",
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
    "notification_interval": (
        "Define the number of 'time units' to wait before re-notifying a contact that this host is still down or unreachable."
        "With the default time unit of 60s, this number will mean multiples of 1 minute."
        "A value of 0 disables re-notifications of contacts about problems for this host - only one problem notification will be sent out."
    ),
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
    "event_handler_enabled": "Indicates whether the event handler is enabled or not",
    "event_handler_command_id": "Event handler command ID",
    "event_handler_command_args": "Event handler command arguments",
    "note_url": "Define an optional URL that can be used to provide more information about the host.",
    "note": "Define an optional note.",
    "action_url": "Define an optional URL that can be used to provide more actions to be performed on the host.",
    "comment": "Comment for this host",
    "categories": "Define the host categories IDs that should be associated with this host",
}


class HostTemplateOrder(BaseOrder):
    model_type: Literal["host_template"] = "host_template"

    field: Literal["name", "alias"] = "name"


class HostTemplateFilter(BaseFilter):
    model_type: Literal["host_template"] = "host_template"

    host_template_id: int | None = Field(default=None, serialization_alias="id $eq")
    host_template_name: str | None = Field(default=None, serialization_alias="name $eq")
    host_template_alias: str | None = Field(default=None, serialization_alias="alias $eq")
    host_template_is_locked: bool | None = Field(default=None, serialization_alias="is_locked $eq")


class HostTemplateBaseParams(BaseParams):
    model_type: Literal["host_template"] = "host_template"

    snmp_community: str | None = Field(None, description=DESCRIPTION["snmp_community"])
    snmp_version: Literal["1", "2c", "3"] | None = Field(
        None, description=DESCRIPTION["snmp_version"]
    )
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
    notification_interval: int | None = Field(
        None, description=DESCRIPTION["notification_interval"]
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
    event_handler_enabled: EnablementStatus | None = Field(
        None, description=DESCRIPTION["event_handler_enabled"]
    )
    event_handler_command_id: int | None = Field(
        None, description=DESCRIPTION["event_handler_command_id"]
    )
    event_handler_command_args: list[str] | None = Field(
        None, description=DESCRIPTION["event_handler_command_args"]
    )
    note_url: str | None = Field(None, description=DESCRIPTION["note_url"])
    note: str | None = Field(None, description=DESCRIPTION["note"])
    action_url: str | None = Field(None, description=DESCRIPTION["action_url"])
    comment: str | None = Field(None, description=DESCRIPTION["comment"])
    categories: list[int] | None = Field(None, description=DESCRIPTION["categories"])


class HostTemplateFullParams(HostTemplateBaseParams):
    name: str = Field(description=DESCRIPTION["name"])
    alias: str = Field(description=DESCRIPTION["alias"])


class HostTemplatePartialParams(HostTemplateBaseParams):
    name: str | None = Field(None, description=DESCRIPTION["name"])
    alias: str | None = Field(None, description=DESCRIPTION["alias"])


class HostTemplate(
    BaseModel,
    ListMixin[HostTemplateFilter, HostTemplateOrder],
    CreateMixin[HostTemplateFullParams],
    PatchMixin[HostTemplatePartialParams],
    DeleteMixin,
):
    endpoint: ClassVar[str] = "configuration/hosts/templates"
    model_type: ClassVar[str] = "host_template"

    id: int
    name: str
    alias: str
    snmp_version: Literal["1", "2c", "3"] | None = None
    timezone_id: int | None = None
    severity_id: int | None = None
    check_command_id: int | None = None
    check_command_args: list[str] | None = None
    check_timeperiod_id: int | None = None
    max_check_attempts: int | None = None
    normal_check_interval: int | None = None
    retry_check_interval: int | None = None
    active_check_enabled: EnablementStatus | None = None
    passive_check_enabled: EnablementStatus | None = None
    notification_enabled: EnablementStatus | None = None
    notification_interval: int | None = None
    notification_timeperiod_id: int | None = None
    add_inherited_contact_group: bool | None = None
    add_inherited_contact: bool | None = None
    first_notification_delay: int | None = None
    recovery_notification_delay: int | None = None
    acknowledgement_timeout: int | None = None
    freshness_checked: EnablementStatus | None = None
    freshness_threshold: int | None = None
    flap_detection_enabled: EnablementStatus | None = None
    low_flap_threshold: int | None = None
    high_flap_threshold: int | None = None
    event_handler_enabled: EnablementStatus | None = None
    event_handler_command_id: int | None = None
    event_handler_command_args: list[str] | None = None
    note_url: str | None = None
    note: str | None = None
    action_url: str | None = None
    comment: str | None = None
    is_locked: bool
