from typing import ClassVar

from pydantic import BaseModel

from centreon_mcp.utils.request import request


class Metric(BaseModel):
    endpoint: ClassVar[str] = "monitoring/hosts/{host_id}/services/{service_id}/metrics"

    id: int
    name: str
    unit: str | None = None
    current_value: float | None = None
    warning_high_threshold: float | None = None
    warning_low_threshold: float | None = None
    critical_high_threshold: float | None = None
    critical_low_threshold: float | None = None

    @classmethod
    async def list(cls, host_id: int, service_id: int) -> list["Metric"]:
        """
        List all metrics of a service with their thresholds and current value.
        """
        endpoint = cls.endpoint.format(host_id=host_id, service_id=service_id)
        content = await request("GET", endpoint)
        return [cls(**item) for item in content]
