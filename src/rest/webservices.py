
def csv_generator(rows, description=None, headers=False, params=None, base=''):
    if headers:
        if type(headers) is str:
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
                    str(value).strip() if type(value) is not str else value.strip()
                )
            elif type(params) is dict:
                line += '%s%s%s' % (
                    base,
                    value.strip() if type(value) is str else str(value).strip(),
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
                v if type(v) is str else str(v)
            )
            yield '%s' % ',' if index < count else ''
        yield '\n\t}'
        yield '%s' % ',' if idx+1 < len(rows) else ''
    yield '\n]'
