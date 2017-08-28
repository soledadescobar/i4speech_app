from django.db import connections


def get_cursor():
    return connections['rest'].cursor()


def to_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
