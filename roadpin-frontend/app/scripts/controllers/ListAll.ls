'use strict'

angular.module 'roadpinFrontendApp'
  .controller 'ListAllCtrl',  <[ $scope $location $rootScope version jsonAll ]> ++ ($scope, $location, $rootScope, version, jsonAll) ->
    $scope <<< {version}

    $scope.the_data_all = []

    #$scope.$watch (-> Object.keys(jsonAll.getData!).length), ->
    #  the_data = jsonAll.getData!
    #  the_data_values = [val for key, val of the_data]
    #  console.log 'the_data_values:', the_data_values
    #  $scope.the_data_all ++= the_data_values

    gridOptionsAll = 
      data: 'the_data_all'
      enablePaging: true
      pageSizes: [10, 100, 1000]
      pageSize: 10
      showFilter: true
      enableColumnResize: true
      enableHighlighting: true
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

    $scope <<< {gridOptionsAll}