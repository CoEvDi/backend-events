from httpx import AsyncClient

from . import exclude_dict_keys


async def ok_200(app):
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.get(
            "/event/1"
        )
    assert response.status_code == 200
    resp = exclude_dict_keys(response.json(), [('content', 'created_time')])
    assert resp == {
        "content": {
            "id": 1,
            "title": "My awesome title",
            "preview": "My awesome body",
            "description": "My awesome description",
            "start_date": "2000-01-01",
            "end_date": "2000-01-01",
            "start_time": "01:01:01",
            "end_time": "02:02:02",
            "location": "My awesome location",
            "site_link": "My awesome site link",
            "additional_info": "My awesome additional info",
            "guests_info": "My awesome guests info",
            "creator_id": 1,
            "viewers_count": 0
        }
    }


async def not_found_404(app):
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.get("/event/404")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "No event with this id"
    }
