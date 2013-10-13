'use strict'

angular.module 'roadpinFrontendApp'
  .controller 'AppCtrl', <[ $scope $location $rootScope version jsonToday ]> ++ ($scope, $location, $rootScope, version, jsonToday) ->
    $scope <<< {version}

    console.log '$location.path():', $location.path()

    $scope.$watch (-> $location.path()), (active-nav-id, orig-active-nav-id) ->
      console.log '$location.path():', $location.path(), 'active-nav-id:', active-nav-id, 'orig-active-nav-id', orig-active-nav-id
      $scope <<< {active-nav-id}

    pageTitle = 'RoadPin'

    getClass = (id) ->
      if $scope.active-nav-id is id then 'active' else ''

    $scope.the_data = []

    $scope.$watch (-> Object.keys(jsonToday.getData!).length), ->
      the_data = jsonToday.getData!
      the_data_values = [val for key, val of the_data]
      console.log 'the_data_values:', the_data_values
      $scope.the_data ++= the_data_values
      console.log '$scope:', $scope

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

    $scope <<< {getClass, gridOptions, pageTitle}
