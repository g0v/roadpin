import json
import os
from IPython import embed
import datetime as dt
import time

DIR = '../taipei-road-case/'


def _parse_date(date, delta=0):
    if not date: return None
    year, month, date = [int(x) for x in date.split('/')]
    year += 1911
    d = dt.datetime(year, month, date) + dt.timedelta(delta)
    return int(time.mktime(d.timetuple()))

if __name__ == '__main__':

    filenames = os.listdir(DIR)
    
    all_data = []
    for filename in filenames:
        f = open(DIR+filename)
        data = json.load(f)[0]
        all_data.append(data)
        f.close()
        raw_date_range = data['WORK_DATEpro']

        print filename, raw_date_range,
        if len(raw_date_range) == 1:
            begin_at = None
            end_at = None
        else:
            begin_str, end_str = raw_date_range.split('~')
            begin_at = _parse_date(begin_str)
            end_at = _parse_date(end_str, delta=1)

        print begin_at, end_at
        
        data['beginAt'] = begin_at
        data['endAt'] = end_at


    #print json_datas
    f = open('road-cases.json', 'w+')
    json.dump(all_data, f)
    f.close()
