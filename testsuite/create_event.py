from httpx import AsyncClient

from . import exclude_dict_keys, replace_dict_kyedata
from .datasets.data_headers import *
from .datasets.data_events_input import *


async def missing_header_401(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post(
            "/event",
            headers=replace_dict_kyedata(
                header_user1,
                [
                    ('COEVDI_ACCOUNT_ID', '')
                ]
            ),
            json=input_event1
        )
        assert response.status_code == 401
        assert response.json() == {
            'detail': 'Missing auth HEADER(S)'
        }


async def missing_field_422(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post(
            "/event",
            headers=header_user1,
            json=replace_dict_kyedata(
                input_event1,
                [
                    ('start_date', ('startdate', '2000-05-01'))
                ]
            )
        )
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": [
                        "body",
                        "start_date"
                    ],
                    "msg":"field required",
                    "type":"value_error.missing"
                }
            ]
        }


async def wrong_datetime_422(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post(
            "/event",
            headers=header_user1,
            json=replace_dict_kyedata(
                input_event1,
                [
                    ('start_time', ('start_time', '01:0101'))
                ]
            )
        )
        assert response.status_code == 422
        assert response.json() == {
            'detail': 'Wrong date or time string(s)'
        }


async def start_date_more_than_end_422(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post(
            "/event",
            headers=header_user1,
            json=replace_dict_kyedata(
                input_event1,
                [
                    ('start_date', ('start_date', '2000-05-02'))
                ]
            )
        )
        assert response.status_code == 422
        assert response.json() == {
            'detail': 'End date should be equal or later start date'
        }


async def start_time_more_than_end_422(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post(
            "/event",
            headers=header_user1,
            json=replace_dict_kyedata(
                input_event1,
                [
                    ('end_time', ('end_time', '01:00:01'))
                ]
            )
        )
        assert response.status_code == 422
        assert response.json() == {
            'detail': 'End time later start time'
        }


async def ok_201(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post(
            "/event",
            headers=header_user1,
            json=input_event1
        )
        assert response.status_code == 201
        assert response.json() == {
            'content': 1
        }


async def ok_5_201(app):
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        # User2 create Event2
        response = await ac.post(
            "/event",
            headers=header_user2,
            json=input_event2
        )
        assert response.status_code == 201
        assert response.json() == {'content': 2}
        # User2 create Event3
        response = await ac.post(
            "/event",
            headers=header_user2,
            json=input_event3
        )
        assert response.status_code == 201
        assert response.json() == {'content': 3}
        # User1 create Event4
        response = await ac.post(
            "/event",
            headers=header_user1,
            json=input_event4
        )
        assert response.status_code == 201
        assert response.json() == {'content': 4}
        # User3 create Event5
        response = await ac.post(
            "/event",
            headers=header_user3,
            json=input_event5
        )
        assert response.status_code == 201
        assert response.json() == {'content': 5}
        # User4 create Event6
        response = await ac.post(
            "/event",
            headers=header_user4,
            json=input_event6
        )
        assert response.status_code == 201
        assert response.json() == {'content': 6}
