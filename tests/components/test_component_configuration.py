from typing import Literal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from centreon_mcp.components.configuration import (
    create_configuration,
    delete_configurations,
    list_configurations,
    update_configuration,
)

MODULE = "centreon_mcp.components.configuration"


@pytest.mark.parametrize(
    "model_type",
    [
        "command",
        "host",
        "host_group",
        "host_category",
        "host_template",
        "host_severity",
        "monitoring_server",
    ],
)
@patch("centreon_mcp.utils.mixins.ListMixin.list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_configurations(
    logger: MagicMock,
    list: AsyncMock,
    model_type: Literal[
        "command",
        "host",
        "host_group",
        "host_category",
        "host_template",
        "host_severity",
        "monitoring_server",
    ],
):

    # Setup args
    filters = [MagicMock()]
    limit = 50
    page = 1
    order = MagicMock()

    # Mock logger
    logger.debug.return_value = None

    model = MagicMock()
    list.return_value = [model]

    # Call test function
    results = await list_configurations(model_type, filters, limit, page, order)

    # Assert ListMixin.list called with right args
    list.assert_awaited_once_with(filters, limit, page, order)

    # Assert result
    assert results == [model]


@pytest.mark.parametrize(
    "model_type",
    ["command", "host_category", "host_group", "host_severity", "host_template", "host"],
)
@patch("centreon_mcp.utils.mixins.CreateMixin.create", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_create_configuration(
    logger: MagicMock,
    create: AsyncMock,
    model_type: Literal[
        "command", "host_category", "host_group", "host_severity", "host_template", "host"
    ],
):

    # Setup args
    params = MagicMock()

    # Mock logger
    logger.info.return_value = None

    # Mock CreateMixin.create
    create.return_value = True

    # Call test function
    result = await create_configuration(model_type, params)

    # Assert  CreateMixin.create called with right args
    create.assert_awaited_once_with(params)

    # Assert result
    assert result


@pytest.mark.parametrize(
    "model_type",
    ["host_category", "host_group", "host_severity"],
)
@patch("centreon_mcp.utils.mixins.PutMixin.update", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_put_configuration(
    logger: MagicMock,
    update_mixin: AsyncMock,
    model_type: Literal["host_category", "host_group", "host_severity"],
):

    # Setup args
    model_id = 10
    params = MagicMock()

    # Mock logger
    logger.info.return_value = None

    # Mock PutMixin.update
    update_mixin.return_value = True

    # Call test function
    result = await update_configuration(model_type, model_id, params)

    # Assert PutMixin.update called with right args
    update_mixin.assert_awaited_once_with(model_id, params)

    # Assert result
    assert result


@pytest.mark.parametrize(
    "model_type",
    ["host_template", "host"],
)
@patch("centreon_mcp.utils.mixins.PatchMixin.update", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_patch_configuration(
    logger: MagicMock,
    update_mixin: AsyncMock,
    model_type: Literal["host", "host_template"],
):

    # Setup args
    model_id = 10
    params = MagicMock()

    # Mock logger
    logger.info.return_value = None

    # Mock PatchMixin.update
    update_mixin.return_value = True

    # Call test function
    result = await update_configuration(model_type, model_id, params)

    # Assert PatchMixin.update called with right args
    update_mixin.assert_awaited_once_with(model_id, params)

    # Assert result
    assert result


@pytest.mark.parametrize(
    "model_type",
    ["host_category", "host_group", "host_severity", "host_template", "host"],
)
@patch("centreon_mcp.utils.mixins.DeleteMixin.delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_delete_configurations(
    logger: MagicMock,
    delete: AsyncMock,
    model_type: Literal["host_category", "host_group", "host_severity", "host_template", "host"],
):

    # Setup args
    model_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock DeleteMixin.delete
    delete.return_value = {model_id: True}

    # Call test function
    result = await delete_configurations(model_type, [model_id])

    # Assert DeleteMixin.delete called with right args
    delete.assert_awaited_once_with([model_id])

    # Assert result
    assert result == {model_id: True}
