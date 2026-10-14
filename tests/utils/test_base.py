import re

import pytest

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseParams, BaseResource

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


@pytest.mark.parametrize(
    "model",
    [BaseOrder, BaseFilter, BaseParams],
)
async def test_base_check(model):

    # Setup args
    model_type = "host"
    instance = model(model_type=model_type)

    # Call test method
    result = instance.check(model_type)

    # Assert result
    assert result is None


@pytest.mark.parametrize(
    "model, label",
    [
        (BaseOrder, "order"),
        (BaseFilter, "filter"),
        (BaseParams, "params"),
    ],
)
async def test_base_check_mismatch(model, label):

    # Setup args
    instance = model(model_type="host")

    # Call test method and assert error
    with pytest.raises(
        ValueError,
        match=re.escape(f"model_type 'service' does not match {label}.model_type 'host'"),
    ):
        instance.check("service")
