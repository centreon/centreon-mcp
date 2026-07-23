from typing import Annotated

from pydantic import Field

from centreon_mcp.types.monitoring.actions.acknowledgement import (
    Acknowledgement,
    AcknowledgementFilter,
    AcknowledgementOrder,
    AcknowledgementParams,
)
from centreon_mcp.types.monitoring.actions.check import CheckParams
from centreon_mcp.types.monitoring.actions.comment import CommentParams
from centreon_mcp.types.monitoring.actions.downtime import (
    Downtime,
    DowntimeFilter,
    DowntimeOrder,
    DowntimeParams,
)

MonitoringActionFilter = Annotated[
    AcknowledgementFilter | DowntimeFilter,
    Field(discriminator="model_type"),
]


MonitoringActionOrder = Annotated[
    AcknowledgementOrder | DowntimeOrder,
    Field(discriminator="model_type"),
]

MonitoringActionParams = Annotated[
    AcknowledgementParams | DowntimeParams | CheckParams | CommentParams,
    Field(discriminator="model_type"),
]


MonitoringAction = Acknowledgement | Downtime
