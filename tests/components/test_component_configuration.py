from typing import Literal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from centreon_mcp.components.configuration import (
    CONFIGURATIONS_FULL_PARAMS,
    create_configuration,
    delete_configurations,
    list_configurations,
    update_configuration,
)
from centreon_mcp.types import (
    MODELS_MIXIN_CREATE,
    MODELS_MIXIN_DELETE,
    MODELS_MIXIN_LIST,
    MODELS_MIXIN_PATCH,
    MODELS_MIXIN_UPDATE,
)

MODULE = "centreon_mcp.components.configuration"


@pytest.mark.parametrize(
    "model_type",
    [
        "command",
        "host_category",
        "host_group",
        "host_severity",
        "host_template",
        "host",
        "monitoring_server",
    ],
)
@patch(f"{MODULE}._list", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_list_configurations(
    logger: MagicMock,
    _list: AsyncMock,
    model_type: Literal[
        "command",
        "host_category",
        "host_group",
        "host_severity",
        "host_template",
        "host",
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

    # Mock _list
    model_cls = MODELS_MIXIN_LIST[model_type]
    model = model_cls.model_construct()
    _list.return_value = [model]

    # Call test function
    results = await list_configurations(model_type, filters, limit, page, order)

    # Assert _list called with right args
    _list.assert_awaited_once_with(model_cls, filters, limit, page, order)

    # Assert result
    assert results == [model]


@pytest.mark.parametrize(
    "model_type",
    ["command", "host_category", "host_group", "host_severity", "host_template", "host"],
)
@patch(f"{MODULE}._create", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_create_configuration(
    logger: MagicMock,
    _create: AsyncMock,
    model_type: Literal[
        "command", "host_category", "host_group", "host_severity", "host_template", "host"
    ],
):

    # Setup args
    params = MagicMock()

    # Mock logger
    logger.info.return_value = None

    # Mock _create
    _create.return_value = True

    # Call test function
    result = await create_configuration(model_type, params)

    # Assert _create called with right args
    _create.assert_awaited_once_with(MODELS_MIXIN_CREATE[model_type], params)

    # Assert result
    assert result


@pytest.mark.parametrize(
    "model_type",
    ["host_category", "host_group", "host_severity"],
)
@patch(f"{MODULE}._update", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_update_configuration_put(
    logger: MagicMock,
    _update: AsyncMock,
    model_type: Literal["host_category", "host_group", "host_severity"],
):

    # Setup args
    model_id = 10
    params = MagicMock()

    # Mock logger
    logger.info.return_value = None

    # Mock _update
    _update.return_value = True

    # Call test function
    result = await update_configuration(model_type, model_id, params)

    # Assert _update called with right args
    full_params_cls = CONFIGURATIONS_FULL_PARAMS[model_type]
    _update.assert_awaited_once_with(
        MODELS_MIXIN_UPDATE[model_type], full_params_cls, model_id, params
    )

    # Assert result
    assert result


@pytest.mark.parametrize(
    "model_type",
    ["host_template", "host"],
)
@patch(f"{MODULE}._patch", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_update_configuration_patch(
    logger: MagicMock,
    _patch: AsyncMock,
    model_type: Literal["host_template", "host"],
):

    # Setup args
    model_id = 10
    params = MagicMock()

    # Mock logger
    logger.info.return_value = None

    # Mock _patch
    _patch.return_value = True

    # Call test function
    result = await update_configuration(model_type, model_id, params)

    # Assert _patch called with right args
    _patch.assert_awaited_once_with(MODELS_MIXIN_PATCH[model_type], model_id, params)

    # Assert result
    assert result


@pytest.mark.parametrize(
    "model_type",
    ["host_category", "host_group", "host_severity", "host_template", "host"],
)
@patch(f"{MODULE}._delete", new_callable=AsyncMock)
@patch(f"{MODULE}.logger", new_callable=MagicMock)
async def test_delete_configurations(
    logger: MagicMock,
    _delete: AsyncMock,
    model_type: Literal["host_category", "host_group", "host_severity", "host_template", "host"],
):

    # Setup args
    model_id = 10

    # Mock logger
    logger.info.return_value = None

    # Mock _delete
    _delete.return_value = {model_id: True}

    # Call test function
    result = await delete_configurations(model_type, [model_id])

    # Assert _delete called with right args
    _delete.assert_awaited_once_with(MODELS_MIXIN_DELETE[model_type], [model_id])

    # Assert result
    assert result == {model_id: True}
