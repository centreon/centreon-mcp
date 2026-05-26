from unittest.mock import AsyncMock, patch

from centreon_mcp.types.host_category import (
    HostCategoryConfiguration,
)

MODULE = "centreon_mcp.types.host_category"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_host_category_configuration_get(request: AsyncMock):

    # Setup args
    host_category = HostCategoryConfiguration.model_construct(
        id=10, name="host_category_name", alias="host_category_alias", is_activated=True
    )

    # Mock request
    request.return_value = host_category.model_dump(mode="json")

    # Call test function
    result = await HostCategoryConfiguration.get(host_category.id)

    # Assert request called with right args
    request.assert_awaited_once_with("GET", f"configuration/hosts/categories/{host_category.id}")

    # Check result
    assert result == host_category
