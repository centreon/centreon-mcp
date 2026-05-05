from centreon_mcp.types.base import StatusCount

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
