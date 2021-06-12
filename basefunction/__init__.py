from operator import itemgetter


def json2list(json_file):
    _list = list()
    for line in json_file:
        _list.append(line['text'])

    return _list


def list2json(idxs, json_file):
    result = list()
    for idx in idxs:
        result.append(json_file[idx])

    return result


def ctrl_f(keyword, json_file):
    keyword_list = keyword.split(' ')
    result = list()
    time = list()
    for word in keyword_list:
        for line in json_file:
            if word in line['text']:
                if line['start'] not in time:
                    result.append(line)
                    time.append(line['start'])
    result = sorted(result, key=itemgetter('start'))
    return result
