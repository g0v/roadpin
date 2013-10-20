'use strict'

angular.module 'roadpinFrontendApp'
  .controller 'MapCtrl', <[ $scope jsonToday geoAccelGyro ]> ++ ($scope, jsonToday, geoAccelGyro) ->
    geo = geoAccelGyro.getGeo!
    console.log 'Map: $scope.mapOptions: geo:', geo

    $scope.mapOptions = 
      center: new google.maps.LatLng geo.lat, geo.lon
      zoom: 14
      mapTypeId: google.maps.MapTypeId.ROADMAP

    is_first_map_center = true
    $scope.$on 'geoAccelGyro:event', (e, data) ->
      console.log 'got geoAccelGyro:event: data:', data, 'is_first_map_center:', is_first_map_center
      if data.event != 'devicegeo'
          return

      if not is_first_map_center
          return

      console.log 'to set is_first_map_center as false'
      is_first_map_center := false

      console.log 'to set scope.mapOptions.center as new center: data:', data
      $scope.myMap.setCenter (new google.maps.LatLng data.lat, data.lon)

    $scope.$watch (-> Object.keys(jsonToday.getData!).length), ->
      the_data = jsonToday.getData!
      the_data_values = [val for key, val of the_data]

      console.log 'Map: the_data_values.length:', the_data_values.length, 'the_data_values:', the_data_values

      my_markers = _parse_markers the_data_values

      $scope.myMarkers = my_markers
      
      #scope.myMarkers = _parse_markers the_data_values

    $scope.onMapIdle = ->


    _parse_markers = (the_data_values) ->
      #console.log 'parse_markers: the_data_values:', the_data_values
      results = [_parse_marker each_value for each_value in the_data_values]
      results = [val for val in results when val is not void]

    _parse_marker = (value) ->
      #console.log '_parse_marker: value', value
      geo = value.geo
      if geo is void
        return void

      [_parse_each_marker(each_geo) for each_geo in geo]

    _parse_each_marker = (geo) ->
      the_type = geo.type
      the_coordinates = geo.coordinates

      #console.log 'geo:', geo, 'the_type:', the_type, 'the_coordinates', the_coordinates
      switch the_type
      | 'Polygon'    => _parse_polygon the_coordinates
      | 'LineString' => _parse_line_string the_coordinates
      | 'Point'      => _parse_point the_coordinates

    _parse_polygon = (coordinates) ->
      polygon_opts = 
        map: $scope.myMap,
        paths: [_parse_path(coord) for coord in coordinates]
        fillColor: \green
        strokeColor: \green

      #console.log 'polygon_opts:', polygon_opts

      polygon = new google.maps.Polygon polygon_opts

    _parse_line_string = (coordinates) ->
      polyline_opts = 
        map: $scope.myMap
        path: _parse_path(coordinates)

      #console.log 'polyline_opts:', polyline_opts

      polyline = new google.maps.Polyline polyline_opts

    _parse_point = (coordinates) -> 
      marker_opts = 
        map: $scope.myMap
        position: new google.maps.LatLng coordinates[1], coordinates[0]

      #console.log 'marker_opts:', marker_opts

      marker = new google.maps.Marker marker_opts

    _parse_path = (coordinates) ->
      [new google.maps.LatLng coord[1], coord[0] for coord in coordinates]

    #console.log 'MapCtrl: end: scope:', $scope
