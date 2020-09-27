from typing import NamedTuple, Type

from django.db import connections
from django.db.models import Model

from report_portal.models import Agent, Organizer, Organization


class SyncParam(NamedTuple):
    sql: str
    model: Type[Model]


_SYNC_DICT = {
    'agents': SyncParam(
        'SELECT id, name, organization_id FROM contractor WHERE contractor_type=\'AGENT\' ORDER BY id', Agent),
    'organizers': SyncParam(
        'SELECT id, name, organization_id FROM contractor WHERE contractor_type=\'ORGANIZER\' ORDER BY id', Organizer),
    'organizations': SyncParam(
        'SELECT id, name FROM organization ORDER BY id', Organization),
}


def sync(sync_object) -> bool:
    if sync_object not in _SYNC_DICT:
        return False

    param = _SYNC_DICT[sync_object]

    with connections['reports'].cursor() as cursor:
        cursor.execute(param.sql)
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    items = []

    for row in rows:
        items.append(param.model(**row))

    if items:
        param.model.objects.bulk_create(items, batch_size=100, ignore_conflicts=True)

    return True
