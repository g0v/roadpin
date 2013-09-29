'use strict'

angular.module 'roadpinFrontendApp'
  .controller 'AppCtrl', <[ $scope $location $resource $rootScope version ]> ++ ($scope, $location, $resource, $rootScope, version) ->
    $scope <<< {version}

    $scope.$watch '$location.path()' (active-nav-id or '/') ->
      $scope <<< {active-nav-id}

    getClass = (id) ->
      if $scope.active-nav-id is id then 'active' else ''

    awesomeThings = <[ AngularJS Yeoman Karma brunch livescript ]>

    url = 'http://106.187.101.193:5346/get_json_today'
    QueryData = $resource url

    the_data = QueryData.query {}, -> 
      console .log 'the_data.length:', the_data.length, 'the_data:', the_data

    '''
    the_data = [
      * county_id: "63"
        county_name: "臺北市"
        end_timestamp: 1419955200, 
        extension: 
          CASE_LOCATIONpro: "基隆路四段"
          CASE_STATUSpro: "2"
          CTR_ONAMEpro: ""
          WORK_DATEpro: "103/01/01~103/12/31"
          CASE_TYPEpro: "6" 
          CASE_RANGEpro: "基隆路三段~羅斯福路"
          CTR_WNAMEpro: "協新營造股份有限公司"
          REG_NAMEpro: "大安區"
          dtResultpro: [
            * P2NAME: null
              GEO_TYPE: "Polygon"
              POINTS: [ 
                * P2: 25.015675259737762
                  P1: 121.54238687689245
                * P2: 25.015364673621825
                  P1: 121.5427080981231
                * P2: 25.010943705473352
                  P1: 121.53744258838049
                * P2: 25.01126944425874
                  P1: 121.53720631914334
                * P2: 25.015151059635382
                  P1: 121.5418922068798
                * P2: 25.015675259737762
                  P1: 121.54238687689245
              ]
              P1NAME: null
              KEY: null
          ]
        geo: [  
          * type: "LineString", 
            coordinates: [  
              [ 121.54238687689245 25.015675259737762 ]
              [ 121.5427080981231 25.015364673621825 ]
              [ 121.53744258838049 25.010943705473352 ]
              [ 121.53720631914334 25.01126944425874 ]
              [ 121.5418922068798 25.015151059635382 ] 
              [ 121.54238687689245 25.015675259737762 ]
            ]
        ]
        start_timestamp: 1388505600
        the_category: "taipei_city_road_case"
        the_id: "taipei_city_road_case_5340"
        the_idx: 5340
        start_date: "2014-01-01"
        end_date: "2014-12-31"
    ]
    '''

    gridOptions = 
      data: 'the_data'
      enablePaging: true
      columnDefs: 
        * field: 'county_name'
          displayName: '縣市'
        * field: 'town_name'
          displayName: '鄉鎮市區'
        * field: 'location'
          displayName: '施工位置'
        * field: 'range'
          displayName: '施工範圍'
        * field: 'beginDate'
          displayName: '開始時間'
        * field: 'endDate'
          displayName: '結束時間'
        * field: 'work_institute'
          displayName: '施工單位'
        * field: 'work_institute2'
          displayName: '(施工相關機構)'

    $scope <<< {getClass, awesomeThings, the_data, gridOptions}
