from typing import Annotated

from pydantic import Field

from centreon_mcp.types.monitoring.status.host import HostStatusCount, HostStatusCountFilter
from centreon_mcp.types.monitoring.status.service import (
    ServiceStatusCount,
    ServiceStatusCountFilter,
)

ResourceStatusCountFilter = Annotated[
    HostStatusCountFilter | ServiceStatusCountFilter,
    Field(discriminator="model_type"),
]


ResourceStatusCount = HostStatusCount | ServiceStatusCount
