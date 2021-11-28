from fastapi import APIRouter, Depends, Response, Query
from fastapi.responses import JSONResponse
from typing import Optional, List

from . import schemas
from . import logic
from .config import cfg
from .utils import auth_required


router = APIRouter()


def HTTPanswer(status_code, description):
    return JSONResponse(
        status_code=status_code,
        content={'content': description},
    )


@router.get('/version')
async def version():
    return HTTPanswer(200, f'Current version - {cfg.VERSION}')


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


@router.put('/event/{event_id}/edit')
async def edit_event(event_id: int,
                     event_data: schemas.EditedEvent,
                     current_user = Depends(auth_required)):
    service_status, participation = await logic.check_permission(current_user,
                                                                 event_id)
    if service_status == 'user':
        if not participation:
            HTTPabort(409, 'Not a part of this event')
        if participation == 'viewer':
            HTTPabort(403, 'Denied permission for edit event')
    await logic.edit_event(event_id, event_data)
    return HTTPanswer(200, 'Successfully edited')


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
        HTTPabort(409, 'Not a part of this event')
    if participation == 'manager':
        HTTPabort(409, "Can't leave event without creator aprovement")
    await logic.leave_event(current_user.account_id, event_id)
    return HTTPanswer(200, 'Successfully leaved')
