'use strict'

angular.module 'roadpinFrontendApp'
  .controller 'MapCtrl', <[ $scope ]> ++ ($scope) ->
    $scope.mapOptions = 
      center: new google.maps.LatLng 25.06, 121.53
      zoom: 14
      mapTypeId: google.maps.MapTypeId.ROADMAP

    '''
    $scope.onMapIdle = ->
      if $scope.myMarkers is void
        marker = new google.maps.Marker do
          map: $scope.myMap,
          position: new google.maps.LatLng 25.1, 121.5
        $scope.myMarkers = [marker, ];
    '''

    console.log 'MapCtrl: end: scope:', $scope
