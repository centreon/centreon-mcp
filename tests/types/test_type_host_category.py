from unittest.mock import AsyncMock, patch

from centreon_mcp.types.host_category import (
    HostCategoryConfiguration,
    HostCategoryConfigurationFullParams,
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


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_host_category_configuration_update(request: AsyncMock):

    # Setup args
    host_category_id = 10
    params = HostCategoryConfigurationFullParams.model_construct()

    # Mock request
    request.return_value = None

    # Call test function
    await HostCategoryConfiguration.update(host_category_id, params)

    # Assert request called with right args
    payload = params.model_dump(mode="json", exclude_none=True)
    request.assert_awaited_once_with(
        "PUT", f"configuration/hosts/categories/{host_category_id}", payload
    )


@patch(f"{MODULE}.request", new_callable=AsyncMock)
async def test_host_category_configuration_delete(request: AsyncMock):

    # Setup args
    host_category_id = 10

    # Mock request
    request.return_value = None

    # Call test function
    await HostCategoryConfiguration.delete(host_category_id)

    # Assert request called with right args
    request.assert_awaited_once_with("DELETE", f"configuration/hosts/categories/{host_category_id}")
