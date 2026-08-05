from centreon_mcp.utils.base import BaseResource

MODULE = "centreon_mcp.utils.base"


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
