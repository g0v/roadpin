'use strict'

angular.module 'roadpinFrontendApp'
  .controller 'ReportCtrl',  <[ $scope geoAccelGyro ]> ++ ($scope, geoAccelGyro) ->
    geo = geoAccelGyro.getGeo!
    console.log 'Map: $scope.mapOptions: geo:', geo

    $scope.camera-status = '我要拍照'
    $scope.no-camera = '我不要拍照'

    $scope.$on 'geoAccelGyro:event', (e, data) ->
      #console.log 'to set geoAccelGyro: data:', data
      $scope.geoAccelGyro <<< data

    $scope.stopCamera = ->
      console.log 'to stop camera'
      

    $scope.report-text = "This is ReportText"
    $scope.geoAccelGyro = {lat: geo.lat, lon: geo.lon, yaw: 0, pitch: 0, roll: 0, move_x: 0, move_y: 0, move_z: 0, 'event': 'none'}
