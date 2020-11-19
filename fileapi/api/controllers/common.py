from flask import url_for


def make_public_url(data, function_name: str, end_field: str = 'uuid'):
    new_data = {}
    values = {}
    for field in data:
        if field != 'id':
            new_data[field] = data[field]
            if field == end_field:
                values[end_field] = data[field]
                new_data['uri'] = url_for(function_name, **values, _external=True)
    return new_data
