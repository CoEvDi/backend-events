#import time
import pytest
import asyncio
#from httpx import AsyncClient

from app import app
from testsuite import service
from testsuite import create_event
from testsuite import get_event
from testsuite import get_all_events


#def teardown_function(function):
#    time.sleep(1)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


pytestmark = pytest.mark.asyncio


def test_get_version_and_perfornm_on_startup_fastapi_event(capsys):
    #with capsys.disabled():
    #    print('some text')
    service.get_version(app)


async def test_service_404_route_not_found():
    await service.wrong_route_404(app)


async def test_service_405_method_not_allowed():
    await service.wrong_method_405(app)


async def test_get_all_events_200_no_events():
    await get_all_events.no_events_200(app)


async def test_create_event_401_missing_header():
    await create_event.missing_header_401(app)


async def test_create_event_422_missing_field():
    await create_event.missing_field_422(app)


async def test_create_event_422_wrong_datetime():
    await create_event.wrong_datetime_422(app)


async def test_create_event_422_start_date_more_than_end():
    await create_event.start_date_more_than_end_422(app)


async def test_create_event_422_start_time_more_than_end():
    await create_event.start_time_more_than_end_422(app)


async def test_create_event_ok():
    await create_event.ok_201(app)


async def test_get_event_404_not_found():
    await get_event.not_found_404(app)


async def test_get_event_ok():
    await get_event.ok_200(app)


async def test_get_all_events_200_one_event():
    await get_all_events.one_event_200(app)


async def test_get_all_events_422_wrong_limit():
    await get_all_events.wrong_limit_422(app)


async def test_get_all_events_422_wrong_offset():
    await get_all_events.wrong_offset_422(app)


async def test_create_events_5_ok():
    await create_event.ok_5_201(app)


async def test_get_all_events_200_all_events():
    await get_all_events.all_events_200(app)


async def test_get_all_events_200_last_event():
    await get_all_events.last_event_200(app)


async def test_get_all_events_200_middle_events():
    await get_all_events.middle_events_200(app)
