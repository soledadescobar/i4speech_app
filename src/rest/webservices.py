# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from datetime import timedelta
from django.utils import timezone


def csv_generator(rows, description=None, headers=False, params=None, base=''):
    if headers:
        if type(headers) is unicode:
            yield '%s\n' % headers
        elif type(headers) is list:
            yield '%s\n' % ','.join(headers)
        elif headers and type(params) is dict:
            line = ''
            values_pos = 0
            for index, value in list(enumerate(description)):
                line += '%s%s%s' % (
                    base,
                    value.name,
                    '.' if value.name in params.get('keys') else ',')
                if value.name in params.get('values') and values_pos == 0:
                    values_pos = index - 1
            line = line.rstrip('.').rstrip(',')
            yield '%s\n' % line

    for row in rows:
        count = 0
        line = ''
        for index, value in list(enumerate(row)):
            if not params:
                line += '%s%s%s' % (
                    base,
                    ',' if count > 0 else '',
                    unicode(value).strip() if type(value) is not unicode else value.strip()
                )
            elif type(params) is dict:
                line += '%s%s%s' % (
                    base,
                    value.strip() if type(value) is unicode else unicode(value).strip(),
                    ',' if index < values_pos else '.'
                )
            count += 1
        line = line.rstrip('.').rstrip(',')
        yield '%s\n' % line


def json_generator(rows):
    yield '['
    for idx, row in list(enumerate(rows)):
        yield '\n\t{'
        count = len(list(row.items()))
        index = 0
        for k, v in list(row.items()):
            index += 1
            yield '\n\t\t"%s": "%s"' % (
                k,
                v if type(v) is unicode else unicode(v)
            )
            yield '%s' % ',' if index < count else ''
        yield '\n\t}'
        yield '%s' % ',' if idx+1 < len(rows) else ''
    yield '\n]'


def json_join_cascade_generator(instance, raw_rows):
    from django.db import connections
    from .cursor import to_dict

    with connections['twistreapy'].cursor() as cursor:
        args = {
            instance.param: tuple(
                i.get(instance.field) for i in raw_rows
            )
        }

        cursor.execute(instance.sql, args)

        rows = to_dict(cursor)

    dates = []
    frentes = []
    count = 0

    # Start the JSON Response #
    yield '[\n'
    for row in rows:
        if row['date'] not in dates:
            dates.append(row['date'])
            frentes = []
            if len(dates) > 1:
                # Closing already inserted object
                yield ']}\n]},'
            yield '{{\n"date": "{}",\n"name": "Frentes",\n"children": [\n'.format(row['date'])
        if row['frente'] not in frentes:
            frentes.append(row['frente'])
            count = 0
            if len(frentes) > 1:
                yield '\n\t]},\n'
            yield '\t{{"name": "{}",\n\t"children": [\n'.format(row['frente'].strip())
        yield '{}\n\t\t{{\n\t\t"name": "{}",\n\t\t"size": "{}",\n\t\t"color": "{}"\n\t\t}}'.format(
            ',' if count > 0 else '',
            row['name'].strip(), row['mentions'], row['color'].strip()
        )
        count += 1

    yield '\n\t]}\n]}\n]'


def csv_join_flare_generator(instance, raw_rows):
    from django.db import connections
    from .cursor import to_dict

    with connections['rest'].cursor() as cursor:
        args = {
            instance.param: tuple(
                i.get(instance.field) for i in raw_rows
            )
        }

        cursor.execute(instance.sql, args)

        rows_list = to_dict(cursor)

    def search(field, name, v):
        for r in rows_list:
            if r[field] == v:
                return r[name]

    res = []

    for row in raw_rows:
        res.append(row.copy())
        value = search(
            instance.field,
            instance.name,
            row.get(instance.field)
        )
        if value is None:
            value = 0
        res[-1].update(
            {instance.name: value}
        )
    yield instance.headers
    yield '\n'
    for row in res:
        yield instance.syntax.format(**row)
        yield '\n'


def tsv_generator(sql=None, params=None, rows=None, description=None):
    if sql:
        from django.db import connections

        with connections['twistreapy'].cursor() as cursor:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            from .cursor import to_dict
            rows = to_dict(cursor)
            description = cursor.description

    for desc in description:
        yield '%s\t' % desc.name

    yield '\n'

    for row in rows:
        for d in description:
            if type(row[d.name]) is float:
                yield '%s\t' % '{0:g}'.format(float(row[d.name]))
            else:
                yield '%s\t' % row[d.name]
        yield '\n'


def bubblecharts_generator(rows, filters=None):
    import importlib

    UserMention = getattr(importlib.import_module('twistreapy.models'), 'UserMention')

    sintax = '{frente__name}.{bloque__name}.{user_id},{menciones},{screen_name},{name},{frente__color}'

    args = {}

    if type(filters) is dict:
        args.update(*filters)

    def count(uid):
        return UserMention.objects.filter(
            user_id=uid,
            *args
        ).count()

    yield 'id,value,screenName,nombreCandidato,colorFrente\n'

    for row in rows:
        row.update({'menciones': count(row.get('user_id'))})
        yield sintax.format(**row)
        yield '\n'


def activity_min_max(ids, model):
    # some_day_last_week = timezone.now().date() - timedelta(days=7)
    # monday_of_last_week = some_day_last_week - timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    # monday_of_this_week = monday_of_last_week + timedelta(days=7)

    objs = model.objects.filter(
        user_id__in=ids,
        created_at__gte=timezone.now().date() - timedelta(days=7),
        # created_at__lt=monday_of_this_week
    )

    values = []

    for uid in ids:
        values.append(objs.filter(user_id=uid).count())

    if not len(values):
        yield '{}'
        return

    yield '{\n'
    yield '\t"max": %d,\n' % sum(values)
    yield '\t"min": %d\n' % min(values)
    yield '}'



