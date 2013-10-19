'use strict'

angular.module 'roadpinFrontendApp'
  .controller 'ReportCtrl',  <[ $scope geoAccelGyro ]> ++ ($scope, geoAccelGyro) ->

    $scope.$on 'geoAccelGyro:event', (e, data) ->
      $scope.geoAccelGyro <<< data
      geoAccelGyro.getGeo!

    $scope.report-text = "This is ReportText"
    $scope.geoAccelGyro = {lat: 0, lon: 0, yaw: 0, pitch: 0, roll: 0, move_x: 0, move_y: 0, move_z: 0}
