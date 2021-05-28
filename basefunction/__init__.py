def json2list(json_file):
    _list = list()
    for line in json_file:
        _list.append(line['text'])

    return _list


def ctrl_f(keyword,json_file):
    TimeStamp=[]
    for line in json_file:
        if keyword in line['text']:
            TimeStamp.append(line['time'])
    
    if len(TimeStamp)==0:
        return None
    
    return TimeStamp
