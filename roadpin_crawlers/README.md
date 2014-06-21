Project
=========
這個 project 的目的是對於各個資料的 crawler.
crawlers 所得到的資訊. 將包含以下資訊:

* county_name: 縣市名
* county_id: [縣市的代號](http://zh.wikipedia.org/wiki/中華民國行政區域及村里代碼)
* the_category: 類別 (ex: 'taipei_city_road_case, 'taipei_city_dig_point')
* the_idx: 這個 record 的 id.
* start_timestamp: 開始時間. (UTC timestamp)
* end_timestamp: 結束時間. (UTC timestamp)
* geo: geo info. 使用 geojson 標示
* town_name: 鄉鎮市區
* location: 施工地址
* range: 施工範圍 (相關的施工路段)
* work_institute: 施工單位
* work_institute2: 相關的施工單位
* status: 狀態
* extension: 更多資訊

crawler 所得到的資料. 以 list of dictionary 的 json 方式將以上資訊 post 到
backend 的 /post_json

backend 會增加以下資訊:

* the_id: 由 the_category 和 the_idx 所組成的 unique id
* json_id: 由 county_name, start_timestamp, end_timestamp, the_id 所組成的可根據 county_name, start_timestamp, end_timestamp sorting 的 unique_id
* beginDate: CST 時區的開始日期.
* endDate: CST 時區的結束日期.
