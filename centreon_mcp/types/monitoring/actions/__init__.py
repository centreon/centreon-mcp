from typing import Annotated

from pydantic import Field

from centreon_mcp.types.monitoring.actions.acknowledgement import (
    Acknowledgement,
    AcknowledgementFilter,
    AcknowledgementOrder,
)
from centreon_mcp.types.monitoring.actions.downtime import (
    Downtime,
    DowntimeFilter,
    DowntimeOrder,
)

MonitoringActionFilter = Annotated[
    AcknowledgementFilter | DowntimeFilter,
    Field(discriminator="model_type"),
]


MonitoringActionOrder = Annotated[
    AcknowledgementOrder | DowntimeOrder,
    Field(discriminator="model_type"),
]


MonitoringAction = Acknowledgement | Downtime
