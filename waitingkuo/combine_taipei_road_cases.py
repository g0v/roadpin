import json
import os
from IPython import embed

DIR = '../taipei-road-case/'

if __name__ == '__main__':

    filenames = os.listdir(DIR)
    
    json_datas = []
    for filename in filenames:
        f = open(DIR+filename)
        json_data = json.load(f)
        #print json_data[0]
        json_datas.append(json_data)
        f.close()

    print json_datas
    f = open('all-taipei-road-cases.json', 'w+')
    json.dump(json_datas, f)
    f.close()
