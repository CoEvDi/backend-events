from httpx import AsyncClient

from . import exclude_dict_keys


async def missing_header_401(app):
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.post(
            "/event",
            headers={
                "COEVDI_SESSION_ID": "1",
                "COEVDI_ACCOUNT_ROLE": "role",
                "COEVDI_LOGIN_TIME": "today",
                "COEVDI_ACCOUNT_CLIENT": "desktop"
            },
            json={
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
                "guests_info": "My awesome guests info"
            }
        )
        assert response.status_code == 401
        assert response.json() == {
            'detail': 'Missing auth HEADER(S)'
        }


async def missing_field_422(app):
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.post(
            "/event",
            headers={
                "COEVDI_ACCOUNT_ID": "1",
                "COEVDI_SESSION_ID": "1",
                "COEVDI_ACCOUNT_ROLE": "role",
                "COEVDI_LOGIN_TIME": "today",
                "COEVDI_ACCOUNT_CLIENT": "desktop"
            },
            json={
                "title": "My awesome title",
                "preview": "My awesome body",
                "description": "My awesome description",
                "startdate": "2000-01-01",
                "end_date": "2000-01-01",
                "start_time": "01:01:01",
                "end_time": "02:02:02",
                "location": "My awesome location",
                "site_link": "My awesome site link",
                "additional_info": "My awesome additional info",
                "guests_info": "My awesome guests info"
            }
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
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.post(
            "/event",
            headers={
                "COEVDI_ACCOUNT_ID": "1",
                "COEVDI_SESSION_ID": "1",
                "COEVDI_ACCOUNT_ROLE": "role",
                "COEVDI_LOGIN_TIME": "today",
                "COEVDI_ACCOUNT_CLIENT": "desktop"
            },
            json={
                "title": "My awesome title",
                "preview": "My awesome body",
                "description": "My awesome description",
                "start_date": "2000-01-01",
                "end_date": "2000-01-01",
                "start_time": "01:0101",
                "end_time": "02:02:02",
                "location": "My awesome location",
                "site_link": "My awesome site link",
                "additional_info": "My awesome additional info",
                "guests_info": "My awesome guests info"
            }
        )
        assert response.status_code == 422
        assert response.json() == {
            'detail': 'Wrong date or time string(s)'
        }


async def start_date_more_than_end_422(app):
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.post(
            "/event",
            headers={
                "COEVDI_ACCOUNT_ID": "1",
                "COEVDI_SESSION_ID": "1",
                "COEVDI_ACCOUNT_ROLE": "role",
                "COEVDI_LOGIN_TIME": "today",
                "COEVDI_ACCOUNT_CLIENT": "desktop"
            },
            json={
                "title": "My awesome title",
                "preview": "My awesome body",
                "description": "My awesome description",
                "start_date": "2000-01-02",
                "end_date": "2000-01-01",
                "start_time": "01:01:01",
                "end_time": "02:02:02",
                "location": "My awesome location",
                "site_link": "My awesome site link",
                "additional_info": "My awesome additional info",
                "guests_info": "My awesome guests info"
            }
        )
        assert response.status_code == 422
        assert response.json() == {
            'detail': 'End date should be equal or later start date'
        }


async def start_time_more_than_end_422(app):
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.post(
            "/event",
            headers={
                "COEVDI_ACCOUNT_ID": "1",
                "COEVDI_SESSION_ID": "1",
                "COEVDI_ACCOUNT_ROLE": "role",
                "COEVDI_LOGIN_TIME": "today",
                "COEVDI_ACCOUNT_CLIENT": "desktop"
            },
            json={
                "title": "My awesome title",
                "preview": "My awesome body",
                "description": "My awesome description",
                "start_date": "2000-01-01",
                "end_date": "2000-01-01",
                "start_time": "01:01:01",
                "end_time": "01:00:01",
                "location": "My awesome location",
                "site_link": "My awesome site link",
                "additional_info": "My awesome additional info",
                "guests_info": "My awesome guests info"
            }
        )
        assert response.status_code == 422
        assert response.json() == {
            'detail': 'End time later start time'
        }


async def ok_201(app):
    async with AsyncClient(app=app, base_url="http://localhost:8003") as ac:
        response = await ac.post(
            "/event",
            headers={
                "COEVDI_ACCOUNT_ID": "1",
                "COEVDI_SESSION_ID": "1",
                "COEVDI_ACCOUNT_ROLE": "role",
                "COEVDI_LOGIN_TIME": "today",
                "COEVDI_ACCOUNT_CLIENT": "desktop"
            },
            json={
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
                "guests_info": "My awesome guests info"
            }
        )
        assert response.status_code == 201
        assert response.json() == {
            'content': 1
        }
