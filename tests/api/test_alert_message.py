import pytest


@pytest.mark.asyncio
async def test_fetch_alert_messages(client, mock_db_session) -> None:
    response = await client.get("/messages/")
    results = response.json()["items"]

    assert response.status_code == 200
    assert response.json() == {
        "items": results,
        "page": 1,
        "pages": 0,
        "size": 5,
        "total": len(results),
    }

    mock_db_session.query.assert_awaited()
