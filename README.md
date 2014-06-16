簡介
==========
這個 project 最先是由 Monjour Chen 所發想而在 g0v.tw 的 hackath3n init 的.

這個 project 有以下的目標:
* 查詢全臺灣在做道路施工的資料.
* 提供大家一個 (或多個) 容易 report 路面不平的方式.

Roadpin.pdf 是 Zoe 所做的關於這個 project 的簡單介紹.
裡面有比較完整的關於這個 project 的說明.

API
==========
以下 link 是之前在 irc 上所討論的 api spec:

https://docs.google.com/spreadsheet/ccc?key=0AlxFjhblzIuidGdaYWRZcEYzRzUzbnhTY2RSczVyWnc#gid=0

目前有一台測試用的機器. 在 106.187.101.193.

目前的 demo:

http://106.187.101.193
* 測試的 front-end

http://106.187.101.193:5346/search_by_location?lat=25.12&lng=121.5&distance=100
* 搜尋 (25.12, 121.5) 範圍 100 公尺內所擁有的資料
* 目前已完成臺北市部分. 將會儘快增加其他縣市的部份.

http://106.187.101.193:5346/report (done by ypcat, helped by Jyun-Fan Tasi)
* 使用 browser report geo/accelerometer data
* user id 是 random gen 的. 不會追蹤到是誰.
* 希望是在開車時. 就能根據所收集到的 data 來幫助決定是否有不平的路面.
* 目前正在 data collection 階段.
* 將會利用 collect 到的 data 來學習如何辨識可能為不平的路面.

Prerequisite:
==========
這個 project 需要有以下的 language/db:

* python 2.7 and pip and virtualenv
  - http://www.python.org/
  - http://www.pip-installer.org/en/latest/installing.html#install-or-upgrade-pip
  - http://www.virtualenv.org/en/latest/virtualenv.html#installation

* node and npm
  - http://nodejs.org/

* mongodb
  - http://www.mongodb.org/

Scripts
==========
目前在 scripts_op 下有以下的 scripts:

* init
  - ./scripts_op/init.sh

* backend server
  - ./scripts_op/backend_server.sh production.ini log.tmp.txt 5346

* frontend server
  - ./scripts_op/frontend_server.sh

Mailing List
==========
如果對於這個 project 有興趣. 歡迎寄信到 roadpin@googlegroups.com 上討論.

很歡迎到 https://groups.google.com/forum/#!forum/roadpin 看看之前的討論.

IRC
==========
目前會定期在每個星期天的 8pm 在 irc 的 #roadpin 跟有興趣的朋友們一起討論.

web 版的 irc:

https://webchat.freenode.net/

http://hack.g0v.tw/irc

IRC 的 logbot: http://106.187.101.193:5000/channel/roadpin (utc time)

參與過的朋友們
==========
在 hackath3n. 有 Monjour Chen, Ronny Wang, Willy Kuo, Zoe Peng, Manic, Brecht, 老蕭的參與.

在 hackath4n. 有老蕭, Jyun-Fan Tsai, ypcat 的參與.

在 hackath6n. 有 A-Han 的參與.

在 post-hackath6n. 有 yangppp 的參與.

臺北市道路施工案件查詢服務網
==========
http://www.road.tcg.gov.tw/ROADRCIS

http://www.road.tcg.gov.tw/ROADRCIS/GetCaseGeo.ashx?CASE_ID=5883

http://www.road.tcg.gov.tw/ROADRCIS/GetDigPoint.ashx?AP_NO=10002050

行政院公共工程委員會全民督工
==========
http://cmdweb.pcc.gov.tw/pccms/pwreport/pccducon_geoeng.peo_entry
