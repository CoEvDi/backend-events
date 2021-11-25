from fastapi import APIRouter, Depends, Response, Query
from fastapi.responses import JSONResponse
from typing import Optional, List

from . import schemas
from . import logic
from .utils import auth_required


router = APIRouter()


def HTTPanswer(status_code, description):
    return JSONResponse(
        status_code=status_code,
        content={'content': description},
    )


# external routes for manage events

@router.post('/event')
async def create_event(event: schemas.InputEvent,
                       current_user = Depends(auth_required)):
    event_id = await logic.create_event(current_user.account_id, event)
    return HTTPanswer(201, event_id)


@router.get('/events/all')
async def get_all_events(offset: Optional[int] = Query(None),
                         limit: Optional[int] = Query(None)):
    data = await logic.get_all_events(offset, limit)
    return HTTPanswer(200, data)


@router.get('/event/{event_id}')
async def get_event(event_id: int):
    data = await logic.get_event(event_id)
    return HTTPanswer(200, data)


@router.get('/event/{event_id}/join')
async def join_event(event_id: int,
                     current_user = Depends(auth_required)):
    _, participation = await logic.check_permission(current_user.account_id,
                                                    current_user.role,
                                                    event_id)
    if participation:
        HTTPabort(409, f'Already joined event as {participation}')
    await logic.join_event(current_user.account_id, event_id, 'viewer')
    return HTTPanswer(200, 'Successfully joined')


@router.get('/event/{event_id}/leave')
async def leave_event(event_id: int,
                      current_user = Depends(auth_required)):
    _, participation = await logic.check_permission(current_user.account_id,
                                                    current_user.role,
                                                    event_id)
    if not participation:
        HTTPabort(409, f'Not a part of this event')
    if participation == 'manager':
        HTTPabort(400, "Can't leave event without creator aprovement")
    await logic.leave_event(current_user.account_id, event_id)
    return HTTPanswer(200, 'Successfully leaved')
