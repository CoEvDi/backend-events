from httpx import AsyncClient

from . import exclude_dict_keys, replace_dict_kyedata, add_dict_keys
from .events_data import output_event1


async def no_events_200(app):
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.get(
            "/events/all"
        )
    assert response.status_code == 200
    assert response.json() == {
        "content":{
            "count": 0,
            "events": []
        }
    }


async def one_event_200(app):
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.get(
            "/events/all"
        )
    assert response.status_code == 200
    assert response.json() == {
        "content":{
            "count": 1,
            "events":[
                output_event1
            ]
        }
    }


async def wrong_offet_or_limit_422(app):
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.get(
            "/events/all?offset=-1&limit=-1"
        )
    assert response.status_code == 422
    assert response.json() == {
        "detail": 'Offset or limit has wrong values'
    }
