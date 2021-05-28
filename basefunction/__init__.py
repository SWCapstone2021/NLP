def json2list(json_file):
    _list = list()
    for line in json_file:
        _list.append(line['text'])

    return _list
