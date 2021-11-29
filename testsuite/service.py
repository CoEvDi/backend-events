from fastapi.testclient import TestClient
from httpx import AsyncClient


def get_version(app):
    with TestClient(app) as client:
        response = client.get("/version")
        assert response.status_code == 200


async def wrong_route_404(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post(
            "/wrong_route"
        )
    assert response.status_code == 404
    assert response.json() == {
        "detail": 'Route not found'
    }


async def wrong_method_405(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post(
            "/events/all"
        )
    assert response.status_code == 405
    assert response.json() == {
        "detail": 'Method Not Allowed'
    }
