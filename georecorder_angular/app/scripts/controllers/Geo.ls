'use strict'

angular.module 'angularBrunchSeedLivescriptBowerApp'
  .controller 'GeoCtrl', <[ $scope ]> ++ ($scope) ->
    $scope.awesomeThings = [
      'HTML5 Boilerplate'
      'AngularJS'
      'Karma'
    ]

    sensor = 
      offset_timestamp: 0
      lat: 0
      lon: 0
      yaw: 0
      pitch: 0
      roll: 0
      x: 0
      y: 0
      z: 0
      extension: {}
