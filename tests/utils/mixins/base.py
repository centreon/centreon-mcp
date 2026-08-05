from collections.abc import Sequence
from unittest.mock import AsyncMock, call, patch

from pydantic import BaseModel

from centreon_mcp.utils.base import BaseFilter, BaseOrder, BaseResource
from centreon_mcp.utils.mixins import (
    CountMixin,
    CreateMixin,
    DeleteMixin,
    ListMixin,
    PatchMixin,
    PutMixin,
    ReadMixin,
    SetMixin,
)
from centreon_mcp.utils.request import CentreonAPIError

MODULE = "centreon_mcp.utils.mixins"


class TestCreateMixinBase:
    __test__ = False

    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_create(
        self, request: AsyncMock, model: type[CreateMixin], params: BaseModel, endpoint: str
    ):

        # Mock request
        request.return_value = None

        # Call test function
        await model.create(params)

        # Assert request called with right args
        payload = params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
        request.assert_awaited_once_with("POST", endpoint, payload)


class TestDeleteMixinBase:
    __test__ = False

    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_delete_(self, request: AsyncMock, model: type[DeleteMixin], endpoint: str):

        # Setup args
        model_id = 10

        # Mock request
        request.return_value = None

        # Call test function
        await model._delete(model_id)

        # Assert request called with right args
        request.assert_awaited_once_with("DELETE", f"{endpoint}/{model_id}")

    @patch(f"{MODULE}.DeleteMixin._delete", new_callable=AsyncMock)
    async def test_delete(self, _delete: AsyncMock, model: type[DeleteMixin], endpoint: str):

        # Setup args
        model_ids = [1, 2, 3]

        # Mock DeleteMixin._delete
        error = CentreonAPIError(404, "fake_url", "GET", {})
        _delete.side_effect = [True, error, True]

        # Call test function
        results = await DeleteMixin.delete(model_ids)

        # Assert DeleteMixin._delete called with right args
        _delete.assert_has_awaits([call(model_id) for model_id in model_ids])

        # Assert result
        assert results == {model_ids[0]: True, model_ids[1]: error, model_ids[2]: True}


class TestPutMixinBase:
    __test__ = False

    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_put(
        self,
        request: AsyncMock,
        endpoint: str,
        model_cls: type[PutMixin],
        model: PutMixin,
        partial_params: BaseModel,
        full_params: BaseModel,
    ):
        # Setup args
        model_id = 10

        # Mock request
        request.return_value = None

        # Call test function
        await model_cls.put(model_id, full_params)

        # Assert request called with right args
        payload = full_params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
        request.assert_awaited_once_with("PUT", f"{endpoint}/{model_id}", payload)

    @patch(f"{MODULE}.PutMixin.put", new_callable=AsyncMock)
    @patch(f"{MODULE}.PutMixin.get", new_callable=AsyncMock)
    async def test_update(
        self,
        get_mixin: AsyncMock,
        put_mixin: AsyncMock,
        endpoint: str,
        model_cls: type[PutMixin],
        model: PutMixin,
        partial_params: BaseModel,
        full_params: BaseModel,
    ):
        # Setup args
        model_id = 10

        # Mock PutMixin.get
        get_mixin.return_value = model

        # Mock PutMixin.put
        put_mixin.return_value = True

        # Call the test method
        await model_cls.update(model_id, partial_params)

        # Assert ReadMixin.get awaited with correct args
        get_mixin.assert_awaited_once_with(model_id)

        # Assert PutMixin.put awaited with correct args
        put_mixin.assert_awaited_once_with(model_id, full_params)


class TestReadMixinBase:
    __test__ = False

    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_get(
        self, request: AsyncMock, model: type[ReadMixin], endpoint: str, payload: dict
    ):

        # Setup args
        model_id = 10

        # Mock request
        request.return_value = payload

        # Call test function
        result = await model.get(model_id)

        # Assert request called with right args
        request.assert_awaited_once_with("GET", f"{endpoint}/{model_id}")

        # Assert result
        assert result == model(**payload)


class TestPatchMixinBase:
    __test__ = False

    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_patch_mixin(
        self, request: AsyncMock, model: type[PatchMixin], params: BaseModel, endpoint: str
    ):

        # Setup args
        model_id = 10

        # Mock request
        request.return_value = None

        # Call test function
        await model.patch(model_id, params)

        # Assert request called with right args
        payload = params.model_dump(mode="json", exclude_none=True, exclude={"model_type"})
        request.assert_awaited_once_with("PATCH", f"{endpoint}/{model_id}", payload)

    @patch(f"{MODULE}.PatchMixin.patch", new_callable=AsyncMock)
    async def test_update(
        self,
        patch_mixin: AsyncMock,
        model: type[PutMixin],
        params: BaseModel,
        endpoint: str,
    ):
        # Setup args
        model_id = 10

        # Mock PatchMixin.patch
        patch_mixin.return_value = None

        # Call test function
        await model.update(model_id, params)

        # Assert PatchMixin.patch called with right args
        patch_mixin.assert_awaited_once_with(model_id, params)


class TestListMixinBase:
    __test__ = False

    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_list(
        self,
        request: AsyncMock,
        model: type[ListMixin],
        filters: Sequence[BaseFilter],
        order: BaseOrder,
        search: str,
        sort_by: str,
        endpoint: str,
        payload: dict,
    ):

        # Setup args
        limit = 10
        page = 1

        # Mock request
        request.return_value = {"result": [payload]}

        # Call test function
        results = await model.list(filters, limit, page, order)

        # Assert request called with right args
        params = {"search": search, "limit": limit, "page": page, "sort_by": sort_by}
        request.assert_awaited_once_with("GET", endpoint, params=params)

        # Assert result
        assert results == [model(**payload)]


class TestSetMixinBase:
    __test__ = False

    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_set(
        self,
        request: AsyncMock,
        model: type[SetMixin],
        params: BaseModel,
        endpoint: str,
        payload: dict,
    ):
        # Setup args
        resources = [BaseResource(type="host", resource_id=20, host_id=20)]

        # Call the test function
        _ = await model.set(params, resources)

        # Assert request called with right args
        payload["resources"] = [{"type": "host", "id": 20, "parent": {"id": 20}}]
        request.assert_awaited_once_with("POST", endpoint, payload)


class TestCountMixinBase:
    __test__ = False

    @patch(f"{MODULE}.request", new_callable=AsyncMock)
    async def test_count(
        self,
        request: AsyncMock,
        model: type[CountMixin],
        filters: Sequence[BaseFilter],
        search: str,
        endpoint: str,
        payload: dict,
    ):

        # Mock request
        request.return_value = payload
        # Call test function
        result = await model.count(filters)

        # Assert request called with right args
        params = {"search": search}
        request.assert_awaited_once_with("GET", endpoint, params=params)

        # Assert result
        assert result == model(**payload)
