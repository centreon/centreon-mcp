from centreon_mcp.utils.base import BaseResource, StatusCount

MODULE = "centreon_mcp.types.base"


async def test_status_count_flatten():

    # Setup args
    data: dict = {
        "ok": {"total": 10},
        "warning": {"total": 10},
        "critical": {"total": 10},
        "unknown": {"total": 10},
        "pending": {"total": 10},
        "total": 50,
    }

    # Call test function
    result = StatusCount.flatten(data)

    # Assert result
    assert result == {
        "ok": 10,
        "warning": 10,
        "critical": 10,
        "unknown": 10,
        "pending": 10,
        "total": 50,
    }


async def test_base_resource_dump():

    # Setup args
    resource_type = "service"
    resource_id = 20
    host_id = 10
    resource = BaseResource(type=resource_type, resource_id=resource_id, host_id=host_id)

    # Call test method
    result = resource.dump()

    # Assert result
    assert result == {"parent": {"id": host_id}, "id": resource_id, "type": resource_type}
