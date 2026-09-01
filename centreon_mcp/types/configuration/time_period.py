from enum import IntEnum
from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseParams
from centreon_mcp.utils.mixins import CreateMixin, DeleteMixin, ListMixin, PutMixin, ReadMixin

DESCRIPTION = {
    "name": "Name for this time period",
    "alias": "Alias for this time period",
    "days": "Days belonging to this time period",
    "exceptions": "List of exceptions to the standard schedule",
    "time_range": """
    
        Defines the periods of time.

        * It can contain one or multiple time ranges.
        * Multiple time ranges must be separated by a comma (`,`).
        * Each time range must follow exactly this format: `{start}-{end}`.
        * `start` is the time at which the time range begins.
        * `end` is the time at which the time range ends.
        * Both `start` and `end` must use the `HH:MM` format (ISO 8601 time format with hours and minutes only).
        * Do not include seconds.
        * Do not use spaces around the comma or the `-` separator.

        Examples:

        * `09:00-12:00` → one time range, from 09:00 to 12:00.
        * `09:00-12:00,14:00-18:30` → two time ranges, from 09:00 to 12:00 and from 14:00 to 18:30.
        * `08:30-10:00,11:00-13:30,15:00-18:00` → three time ranges during the day.
        """,
    "day_range": """

        Defines one or multiple specific calendar dates.

            * Each date must be written in ISO 8601 date format: `YYYY-MM-DD`.
            * Multiple dates must be separated by commas (`,`).
            * Do not include spaces around the commas.

            Examples:

            * `2026-09-01` → one date.
            * `2026-09-01,2026-09-15` → two dates.
            * `2026-09-01,2026-09-15,2026-10-01` → three dates.
    """,
}


class WeekDay(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Day(BaseModel):
    day: WeekDay
    time_range: str = Field(description=DESCRIPTION["time_range"])


class TimePeriodException(BaseModel):
    day_range: str = Field(description=DESCRIPTION["day_range"])
    time_range: str = Field(description=DESCRIPTION["time_range"])


class TimePeriodOrder(BaseOrder):
    model_type: Literal["time_period"] = "time_period"

    field: Literal["name", "alias"] = "name"


class TimePeriodFilter(BaseFilter):
    model_type: Literal["time_period"] = "time_period"

    time_period_id: int | None = Field(default=None, serialization_alias="id $eq")
    time_period_name: str | None = Field(default=None, serialization_alias="name $eq")
    time_period_alias: str | None = Field(default=None, serialization_alias="alias $eq")


class TimePeriodBaseParams(BaseParams):
    model_type: Literal["time_period"] = "time_period"

    templates: list[int] = Field(default_factory=list)


class TimePeriodFullParams(TimePeriodBaseParams):
    name: str = Field(description=DESCRIPTION["name"])
    alias: str = Field(description=DESCRIPTION["alias"])
    days: list[Day] = Field(description=DESCRIPTION["days"])
    exceptions: list[TimePeriodException] = Field(description=DESCRIPTION["exceptions"])


class TimePeriodPartialParams(TimePeriodBaseParams):
    name: str | None = Field(default=None, description=DESCRIPTION["name"])
    alias: str | None = Field(default=None, description=DESCRIPTION["alias"])
    days: list[Day] | None = Field(default=None, description=DESCRIPTION["days"])
    exceptions: list[TimePeriodException] | None = Field(default=None, description=DESCRIPTION["exceptions"])


class TimePeriod(
    BaseModel,
    CreateMixin[TimePeriodFullParams],
    PutMixin[TimePeriodPartialParams, TimePeriodFullParams],
    DeleteMixin,
    ReadMixin,
    ListMixin[TimePeriodFilter, TimePeriodOrder],
):
    endpoint: ClassVar[str] = "configuration/timeperiods"
    model_type: ClassVar[str] = "time_period"
    full_params_cls: ClassVar[type[TimePeriodFullParams]] = TimePeriodFullParams

    id: int
    name: str
    alias: str
    days: list[Day]
    exceptions: list[TimePeriodException]
