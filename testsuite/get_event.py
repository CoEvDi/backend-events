from httpx import AsyncClient

from . import exclude_dict_keys, add_dict_keys
from .events_data import input_event1


async def ok_200(app):
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.get(
            "/event/1"
        )
    assert response.status_code == 200
    resp = exclude_dict_keys(response.json(), [('content', 'created_time')])
    assert resp == {
        "content": add_dict_keys(
            input_event1,
            [
                ('id', 1),
                ('creator_id', 1),
                ('viewers_count', 0)
            ]
        )
    }


async def not_found_404(app):
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.get(
            "/event/404"
        )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "No event with this id"
    }
