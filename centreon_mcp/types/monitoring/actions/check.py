from typing import ClassVar, Literal

from pydantic import BaseModel, Field

from centreon_mcp.utils.mixins import SetMixin


class CheckParams(BaseModel):
    model_type: Literal["check"] = "check"

    is_forced: bool = Field(
        True,
        description=(
            "When `is_forced` is True, the check is executed immediately regardless of the configured check interval."
            "Otherwise, the check is scheduled for the next available execution slot.)"
        ),
    )


class Check(BaseModel, SetMixin[CheckParams]):
    endpoint: ClassVar[str] = "monitoring/resources/check"
    set_endpoint: ClassVar[str] = "monitoring/resources/check"
    model_type: ClassVar[str] = "check"
