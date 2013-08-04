
from app.value_map import COUNTY_MAP
from app import util

def process_data(county_name, the_category, the_idx, start_timestamp, end_timestamp, geo, the_data):
    if the_data.__class__.__name__ == 'dict':
        _process_data_core(county_name, the_category, the_idx, start_timestamp, end_timestamp, geo, the_data)
    elif the_data.__class__.__name__ == 'list':
        for (each_idx, each_data) in enumerate(the_data):
            str_idx = str(the_idx) + '.' + str(each_idx)
            num_idx = util._float(str_idx)
            _process_data_core(county_name, the_category, num_idx, start_timestamp, end_timestamp, geo, the_data)


def _process_data_core(county_name, the_category, the_idx, start_timestamp, end_timestamp, geo, the_data):
    data = {'the_id': str(the_category) + '_' + str(the_idx),
            'the_category': the_category,
            'the_idx': the_idx,
            'county_name': county_name,
            'county_id': COUNTY_MAP.get(county_name, county_name),
            'start_timestamp': start_timestamp,
            'end_timestamp': end_timestamp,
            'geo': geo,
            'extension': the_data}
    _put_to_db(data)


def _put_to_db(the_val):
    the_key = {'the_id': the_val['the_id']}
    util.db_update('roadDB', the_key, the_val)
