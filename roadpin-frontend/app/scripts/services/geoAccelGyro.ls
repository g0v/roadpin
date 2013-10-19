'use strict'

angular.module 'roadpinFrontendApp'
  .factory 'geoAccelGyro', <[ $rootScope $window ]> ++ ($rootScope, $window) ->
    console.log 'to set send-event'

    $window.ondeviceorientation = (event) ->
      yaw = event.alpha
      pitch = event.beta
      roll = event.gamma

      $rootScope.$apply -> do
        $rootScope.$broadcast 'geoAccelGyro:event', {'event': 'deviceorientation', yaw, pitch, roll}

    $window.ondevicemotion = (event) ->
      move_x = event.acceleration.x
      move_y = event.acceleration.y
      move_z = event.acceleration.z

      $rootScope.$apply -> do
        $rootScope.$broadcast 'geoAccelGyro:event', {'event': 'devicemotion', move_x, move_y, move_z}

    do 
      getGeo: ->
        console.log 'to getCurrentPosition'
        navigator.geolocation.getCurrentPosition (position) ->
          lat = position.coords.latitude
          lon = position.coords.longitude

          console.log 'got currentPosition: position:', position

          $rootScope.$apply -> do
            $rootScope.$broadcast 'geoAccelGyro:event', {'event': 'devicegeo', lat, lon}
