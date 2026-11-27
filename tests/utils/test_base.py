import re

import pytest
from helpers import filter_classes
from pydantic import Field, ValidationError

from centreon_mcp.utils.base import (
    LIKE_OPERATORS,
    BaseFilter,
    BaseOrder,
    BaseParams,
    BaseResource,
)

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


class Filter(BaseFilter):
    pattern: str | None = Field(default=None, serialization_alias="pattern $lk")
    excluded: str | None = Field(
        default=None, serialization_alias="excluded $nk", description="Excluded value."
    )
    exact: int | None = Field(default=None, serialization_alias="exact $eq")


LIKE_FIELDS = [
    pytest.param(cls, name, field.serialization_alias, id=f"{cls.__qualname__}.{name}")
    for cls in filter_classes()
    for name, field in cls.model_fields.items()
    if field.serialization_alias and field.serialization_alias.split()[-1] in LIKE_OPERATORS
]


@pytest.mark.parametrize("model, field, alias", LIKE_FIELDS)
async def test_base_filter_like_field(model, field, alias):

    # Setup args
    name, operator = alias.split()

    # Call test method
    result = model(**{field: "srv-%"}).conditions

    # Assert result: the pattern is sent as given and the field tells the LLM it is a pattern
    assert result == [{name: {operator: "srv-%"}}]
    assert LIKE_OPERATORS[operator] in model.model_fields[field].description


@pytest.mark.parametrize(
    "value, expected",
    [
        (
            "srv-01",
            [
                {"pattern": {"$lk": "srv-01"}},
                {"excluded": {"$nk": "srv-01"}},
            ],
        ),
        (
            "%web%",
            [
                {"pattern": {"$lk": "%web%"}},
                {"excluded": {"$nk": "%web%"}},
            ],
        ),
        (None, []),
    ],
)
async def test_base_filter_conditions_keep_values(value, expected):

    # Setup args
    instance = Filter(model_type="filter", pattern=value, excluded=value)

    # Call test method
    result = instance.conditions

    # Assert result: LIKE values are sent unchanged, wildcards are up to the caller
    assert result == expected


async def test_base_filter_like_description():

    # Setup args
    schema = Filter.model_json_schema()["properties"]

    # Assert result: LIKE fields get the hint, appended to an existing description, once
    assert schema["pattern"]["description"] == LIKE_OPERATORS["$lk"]
    assert schema["excluded"]["description"] == f"Excluded value. {LIKE_OPERATORS['$nk']}"
    assert "description" not in schema["exact"]

    class SubFilter(Filter):
        pass

    assert SubFilter.model_fields["excluded"].description.count(LIKE_OPERATORS["$nk"]) == 1


async def test_base_filter_forbid_unknown_field():

    # Call test method and assert error: an unknown field must not silently widen the search
    with pytest.raises(ValidationError, match="name"):
        Filter.model_validate({"model_type": "filter", "name": "srv-01"})


async def test_base_filter_join():

    # Setup args
    filters = [Filter(model_type="filter", pattern="srv-%"), Filter(model_type="filter")]
    filters.append(Filter(model_type="filter", exact=1, excluded="%test%"))

    # Call test method
    result = BaseFilter.join(filters)

    # Assert result: filters are OR-ed, their fields AND-ed, empty filters dropped
    assert result == {
        "$or": [
            {"$and": [{"pattern": {"$lk": "srv-%"}}]},
            {"$and": [{"excluded": {"$nk": "%test%"}}, {"exact": {"$eq": 1}}]},
        ]
    }


@pytest.mark.parametrize("filters", [None, []])
async def test_base_filter_join_empty(filters):

    # Call test method and assert result
    assert BaseFilter.join(filters) == {}
