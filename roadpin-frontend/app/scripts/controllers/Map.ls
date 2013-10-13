'use strict'

angular.module 'roadpinFrontendApp'
  .controller 'MapCtrl', <[ $scope jsonToday ]> ++ ($scope, jsonToday) ->
    $scope.mapOptions = 
      center: new google.maps.LatLng 25.06, 121.53
      zoom: 14
      mapTypeId: google.maps.MapTypeId.ROADMAP

    $scope.$watch (-> Object.keys(jsonToday.getData!).length), ->
      the_data = jsonToday.getData!
      the_data_values = [val for key, val of the_data]

      console.log 'the_data_values.length:', the_data_values.length, 'the_data_values:', the_data_values
      
      #scope.myMarkers = _parse_markers the_data_values
      
    $scope.onMapIdle = ->
      if $scope.myMarkers is void
        marker = new google.maps.Marker do
          map: $scope.myMap,
          position: new google.maps.LatLng 25.06, 121.53
        $scope.myMarkers = [marker, ];

    console.log 'MapCtrl: end: scope:', $scope
