from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseParams, EnablementStatus, Link, Macro
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, PatchMixin

DESCRIPTION = {
    "name": "Service name",
    "host_id": "ID of the host linked to this service",
    "geo_coords": "Geographic coordinates of the service",
    "comment": "Service comment",
    "service_template_id": "Template ID of the service template",
    "check_command_id": "Check command ID",
    "check_command_args": "Check command arguments",
    "check_timeperiod_id": "Time period ID of the check command",
    "max_check_attempts": "Define the number of times that the monitoring engine will retry the service check command if it returns any non-OK state",
    "normal_check_interval": (
        "Define the number of 'time units' between regularly scheduled checks of the service."
        "With the default time unit of 60s, this number will mean multiples of 1 minute."
    ),
    "retry_check_interval": (
        "Define the number of 'time units' to wait before scheduling a re-check for this service after a non-OK state was detected."
        "With the default time unit of 60s, this number will mean multiples of 1 minute."
        "Once the service has been retried max_check_attempts times without a change in its status, it will revert to being scheduled at its 'normal' check interval rate."
    ),
    "active_check_enabled": "Indicates whether active checks are enabled or not",
    "passive_check_enabled": "Indicates whether passive checks are enabled or not",
    "volatility_enabled": "Indicates whether the service is 'volatile' or not",
    "notification_enabled": "Specify whether notifications are enabled or not",
    "is_contact_additive_inheritance": (
        "Only used when notification inheritance for hosts and services is set to vertical inheritance only."
        "When enabled, the contact definition will not override the definitions on template levels, it will be appended instead."
    ),
    "is_contact_group_additive_inheritance": (
        "Only used when notification inheritance for hosts and services is set to vertical inheritance only."
        "When enabled, the contactgroup definition will not override the definitions on template levels, it will be appended instead."
    ),
    "notification_interval": (
        "Define the number of 'time units' to wait before re-notifying a contact that this service is still down or unreachable."
        "With the default time unit of 60s, this number will mean multiples of 1 minute."
        "A value of 0 disables re-notifications of contacts about problems for this service - only one problem notification will be sent out."
    ),
    "notification_timeperiod_id": "Notification timeperiod ID",
    "notification_type": (
        "Define the states of the service for which notifications should be sent out."
        "The value is the sum of all the values of the selected options: WARNING=1, UNKNOWN=2, CRITICAL=4, RECOVERY=8, FLAPPING=16, DOWNTIME_SCHEDULED=32, NONE=0."
        "A null value means inheritance of its parent's value; if there is no parent, the value will be assumed to be WARNING|UNKNOWN|CRITICAL|RECOVERY|FLAPPING|DOWNTIME_SCHEDULED."
        "Example: a value of 5 corresponds to the selected options WARNING and CRITICAL."
    ),
    "first_notification_delay": (
        "Define the number of 'time units' to wait before sending out the first problem notification when this service enters a non-OK state."
        "With the default time unit of 60s, this number will mean multiples of 1 minute."
    ),
    "recovery_notification_delay": (
        "Define the number of 'time units' to wait before sending out the recovery notification when this service enters an OK state."
        "With the default time unit of 60s, this number will mean multiples of 1 minute."
    ),
    "acknowledgement_timeout": "Specify a duration of acknowledgement for this service.",
    "freshness_checked": "Indicates whether freshness is checked or not",
    "freshness_threshold": "Specify the freshness threshold (in seconds) for this service.",
    "flap_detection_enabled": "Indicates whether the flap detection is enabled or not",
    "low_flap_threshold": "Specify the low state change threshold used in flap detection for this service",
    "high_flap_threshold": "Specify the high state change threshold used in flap detection for this service",
    "event_handler_enabled": "Indicates whether the event handler is enabled or not",
    "event_handler_command_id": "Event handler command ID",
    "event_handler_command_args": "Event handler command arguments",
    "graph_template_id": "ID of the default graph template that will be used for this service",
    "note": "Define an optional note.",
    "note_url": "Define an optional URL that can be used to provide more information about the service.",
    "action_url": "Define an optional URL that can be used to specify actions to be performed on the service.",
    "icon_id": "Define the image ID that should be associated with this service.",
    "icon_alternative": "Define an optional string that is used as an alternative description for the icon.",
    "severity_id": "Severity ID",
    "is_activated": "Indicates whether the service is activated or not",
    "service_categories": "IDs of service categories linked to this service",
    "service_groups": "IDs of service groups linked to this service",
    "macros": (
        "Macros defined for the service (directly or through a template or command inheritance)."
        "If multiple macros are defined with the same name, only the last one will be saved."
    ),
}


class ServiceOrder(BaseOrder):
    model_type: Literal["service"] = "service"

    field: Literal["id", "name"] = "name"


class ServiceFilter(BaseFilter):
    model_type: Literal["service"] = "service"

    name: str | None = Field(default=None, serialization_alias="name $eq")
    host_id: int | None = Field(default=None, serialization_alias="host.id $eq")
    host_name: str | None = Field(default=None, serialization_alias="host.name $eq")
    service_category_id: int | None = Field(default=None, serialization_alias="category.id $eq")
    service_category_name: str | None = Field(default=None, serialization_alias="category.name $eq")
    severity_id: int | None = Field(default=None, serialization_alias="severity.id $eq")
    severity_name: str | None = Field(default=None, serialization_alias="severity.name $eq")
    service_group_id: int | None = Field(default=None, serialization_alias="group.id $eq")
    service_group_name: str | None = Field(default=None, serialization_alias="group.name $eq")
    host_group_id: int | None = Field(default=None, serialization_alias="hostgroup.id $eq")
    host_group_name: str | None = Field(default=None, serialization_alias="hostgroup.name $eq")
    host_category_id: int | None = Field(default=None, serialization_alias="hostcategory.id $eq")
    host_category_name: str | None = Field(
        default=None, serialization_alias="hostcategory.name $eq"
    )


class ServiceBaseParams(BaseParams):
    model_type: Literal["service"] = "service"

    geo_coords: str | None = Field(None, description=DESCRIPTION["geo_coords"])
    comment: str | None = Field(None, description=DESCRIPTION["comment"])
    service_template_id: int | None = Field(None, description=DESCRIPTION["service_template_id"])
    check_command_id: int | None = Field(None, description=DESCRIPTION["check_command_id"])
    check_command_args: list[str] | None = Field(
        None, description=DESCRIPTION["check_command_args"]
    )
    check_timeperiod_id: int | None = Field(None, description=DESCRIPTION["check_timeperiod_id"])
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
    volatility_enabled: EnablementStatus | None = Field(
        None, description=DESCRIPTION["volatility_enabled"]
    )
    notification_enabled: EnablementStatus | None = Field(
        None, description=DESCRIPTION["notification_enabled"]
    )
    is_contact_additive_inheritance: bool | None = Field(
        None, description=DESCRIPTION["is_contact_additive_inheritance"]
    )
    is_contact_group_additive_inheritance: bool | None = Field(
        None, description=DESCRIPTION["is_contact_group_additive_inheritance"]
    )
    notification_interval: int | None = Field(
        None, description=DESCRIPTION["notification_interval"]
    )
    notification_timeperiod_id: int | None = Field(
        None, description=DESCRIPTION["notification_timeperiod_id"]
    )
    notification_type: int | None = Field(None, description=DESCRIPTION["notification_type"])
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
    graph_template_id: int | None = Field(None, description=DESCRIPTION["graph_template_id"])
    note: str | None = Field(None, max_length=65535, description=DESCRIPTION["note"])
    note_url: str | None = Field(None, max_length=65535, description=DESCRIPTION["note_url"])
    action_url: str | None = Field(None, max_length=65535, description=DESCRIPTION["action_url"])
    icon_id: int | None = Field(None, description=DESCRIPTION["icon_id"])
    icon_alternative: str | None = Field(
        None, max_length=200, description=DESCRIPTION["icon_alternative"]
    )
    severity_id: int | None = Field(None, description=DESCRIPTION["severity_id"])
    is_activated: bool | None = Field(None, description=DESCRIPTION["is_activated"])
    service_categories: list[int] | None = Field(
        None, description=DESCRIPTION["service_categories"]
    )
    service_groups: list[int] | None = Field(None, description=DESCRIPTION["service_groups"])
    macros: list[Macro] | None = Field(None, description=DESCRIPTION["macros"])


class ServiceFullParams(ServiceBaseParams):
    name: str = Field(description=DESCRIPTION["name"])
    host_id: int = Field(description=DESCRIPTION["host_id"])


class ServicePartialParams(ServiceBaseParams):
    name: str | None = Field(None, description=DESCRIPTION["name"])
    host_id: int | None = Field(None, description=DESCRIPTION["host_id"])


class Service(
    BaseModel,
    CreateMixin[ServiceFullParams],
    PatchMixin[ServicePartialParams],
    ListMixin[ServiceFilter, ServiceOrder],
    DeleteMixin,
):
    endpoint: ClassVar[str] = "configuration/services"
    model_type: ClassVar[str] = "service"

    id: int
    name: str
    hosts: list[Link] | None = None
    service_template: Link | None = None
    check_timeperiod: Link | None = None
    notification_timeperiod: Link | None = None
    severity: Link | None = None
    categories: list[Link]
    groups: list[Link]
    normal_check_interval: int | None = None
    retry_check_interval: int | None = None
    is_activated: bool
