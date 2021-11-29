from httpx import AsyncClient

from . import exclude_dict_keys, replace_dict_kyedata, add_dict_keys
from .datasets.data_events_output import *


async def no_events_200(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
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
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
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


async def wrong_limit_422(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get(
            "/events/all?offset=-1&limit=0"
        )
    assert response.status_code == 422
    assert response.json() == {
        "detail": 'Limit lower than 1'
    }


async def wrong_offset_422(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get(
            "/events/all?offset=-1&limit=1"
        )
    assert response.status_code == 422
    assert response.json() == {
        "detail": 'Offset lower than 0'
    }


async def all_events_200(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get(
            "/events/all"
        )
    assert response.status_code == 200
    assert response.json() == {
        "content":{
            "count": 6,
            "events":[
                output_event6,
                output_event4,
                output_event3,
                output_event1,
                output_event2,
                output_event5
            ]
        }
    }


async def last_event_200(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get(
            "/events/all?limit=1"
        )
    assert response.status_code == 200
    assert response.json() == {
        "content":{
            "count": 1,
            "events":[
                output_event6
            ]
        }
    }


async def middle_events_200(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.get(
            "/events/all?limit=2&offset=2"
        )
    assert response.status_code == 200
    assert response.json() == {
        "content":{
            "count": 2,
            "events":[
                output_event3,
                output_event1
            ]
        }
    }
