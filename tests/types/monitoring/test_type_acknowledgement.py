from unittest.mock import AsyncMock, patch

from centreon_mcp.types.monitoring.actions.acknowledgement import Acknowledgement

MODULE = "centreon_mcp.types.monitoring.actions.acknowledgement"


@patch(f"{MODULE}.request", new_callable=AsyncMock)
@patch(f"{MODULE}.Acknowledgement.get", new_callable=AsyncMock)
async def test_acknowledgement_delete_(acknowledgement_get: AsyncMock, request: AsyncMock):

    # Setup args
    model_id = 1
    host_id = 10
    service_id = 20

    # Mock Acknwoledgement.get to return a fake acknowledgement
    acknowledgement = Acknowledgement(
        id=model_id,
        host_id=host_id,
        service_id=service_id,
        author_id=10,
        author_name="author",
        comment="comment",
    )
    acknowledgement_get.return_value = acknowledgement

    # Mock request
    request.return_value = None

    # Call test function
    await Acknowledgement._delete(model_id)

    # Assert Acknowledgement.get awaited with correct args
    acknowledgement_get.assert_awaited_once_with(model_id)

    # Assert request called with right args
    payload = {
        "disacknowledgement": {"with_services": False},
        "resources": [{"parent": {"id": host_id}, "id": service_id, "type": "service"}],
    }
    request.assert_awaited_once_with(
        "DELETE", "monitoring/resources/acknowledgements", payload=payload
    )
