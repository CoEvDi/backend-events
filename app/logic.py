from datetime import datetime, time, date, timedelta
from sqlalchemy.sql import select
from sqlalchemy import func, desc

from .database import events, participants
from .database import _engine
from .config import cfg
from .errors import HTTPabort


def get_datetimes(event):
    try:
        if event.start_date:
            event.start_date = date.fromisoformat(event.start_date)
        if event.end_date:
            event.end_date = date.fromisoformat(event.end_date)
        if event.start_time:
            event.start_time = time.fromisoformat(event.start_time)
        if event.end_time:
            event.end_time = time.fromisoformat(event.end_time)
    except ValueError:
        HTTPabort(422, 'Wrong date or time string(s)')
    return event


async def create_event(account_id, event):
    event = get_datetimes(event)

    if event.start_date > event.end_date:
        HTTPabort(422, 'End date should be equal or later start date')
    if (event.start_date == event.end_date
        and event.start_time > event.end_time):
        HTTPabort(422, 'End time later start time')
    event_data = event.dict()
    event_data['created_time'] = datetime.utcnow()

    async with _engine.begin() as conn:
        query = events.insert().values(
            event_data
        )
        result = await conn.execute(query)
        event_id = result.inserted_primary_key[0]

        query = participants.insert().values(
            event_id=event_id,
            account_id=account_id,
            role='creator',
            joined_time=datetime.utcnow()
        )
        await conn.execute(query)

        return event_id


async def get_all_events(offset=None, limit=None):
    async with _engine.begin() as conn:
        query = select(events).order_by(
            desc(events.c.start_date),
            desc(events.c.start_time)
        )
        if limit is not None:
            if limit < 1:
                HTTPabort(422, 'Limit lower than 1')
            else:
                query = query.limit(limit)
        if offset is not None:
            if offset < 0:
                HTTPabort(422, 'Offset lower than 0')
            else:
                query = query.offset(offset)
        result = await conn.execute(query)

        all_events = []
        count = 0
        for event in result:
            count += 1
            all_events.append({
                'id': event.id,
                'title': event.title,
                'preview': event.preview,
                'location': event.location,
                'start_date': event.start_date.isoformat(),
                'start_time': event.start_time.isoformat()
            })
        return {'count': count, 'events': all_events}


async def get_event(event_id):
    async with _engine.begin() as conn:
        query = select(['*']).select_from(
            events.join(participants,
                        participants.c.role == 'creator')
        ).where(
            events.c.id == event_id
        )
        result = await conn.execute(query)
        event = result.first()
        if not event:
            HTTPabort(404, 'No event with this id')

        query = select(func.count(participants.c.participation_id)).where(
            participants.c.event_id == event_id,
            participants.c.role == 'viewer'
        )
        result = await conn.execute(query)
        viewers_count = result.fetchone().count

        return {
            'id': event.id,
            'title': event.title,
            'preview': event.preview,
            'description': event.description,
            'start_date': event.start_date.isoformat(),
            'end_date': event.end_date.isoformat(),
            'start_time': event.start_time.isoformat(),
            'end_time': event.end_time.isoformat(),
            'location': event.location,
            'site_link': event.site_link,
            'additional_info': event.additional_info,
            'guests_info': event.guests_info,
            'created_time': event.created_time.isoformat(),
            'creator_id': event.account_id,
            'viewers_count': viewers_count
        }


async def edit_event(event_id, event_data):
    event_data = get_datetimes(event_data)
    update_data = {}
    for key, value in event_data:
        if value:
            update_data[key] = value
    async with _engine.begin() as conn:
        query = events.update().where(
            events.c.id == event_id
        ).values(
            update_data
        )
        await conn.execute(query)


async def check_permission(current_user, event_id):
    status = 'user'
    if current_user.role in ('admin', 'moderator'):
        status = 'staff'

    async with _engine.begin() as conn:
        query = select(events).where(
            events.c.id == event_id
        )
        result = await conn.execute(query)
        event = result.first()
        if not event:
            HTTPabort(404, 'No event with this id')

        query = select(participants).where(
            participants.c.event_id == event_id,
            participants.c.account_id == current_user.account_id,
        )
        result = await conn.execute(query)
        participation = result.first()

        part = ''
        if participation:
            part = participation.role

        return (status, part)


async def join_event(account_id, event_id, role):
    async with _engine.begin() as conn:
        query = participants.insert().values(
            event_id=event_id,
            account_id=account_id,
            role=role,
            joined_time=datetime.utcnow()
        )
        await conn.execute(query)


async def leave_event(account_id, event_id):
    async with _engine.begin() as conn:
        conn.execute(participation.delete().where(
            participation.c.account_id == account_id
        ))
