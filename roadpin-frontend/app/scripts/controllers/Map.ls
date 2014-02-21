'use strict'

{map, fold, fold1} = require 'prelude-ls'

COLOR_MAP =
  taipei_city_road_case: \#F08
  taipei_city_dig_point: \#808
  new_taipei_city_dig_point: \#808
  kaohsiung_dig_point: \#808

angular.module 'roadpinFrontendApp'
  .controller 'MapCtrl', <[ $scope jsonToday geoAccelGyro distVincenty distList ]> ++ ($scope, jsonToday, geoAccelGyro, distVincenty, distList) ->
    geo = geoAccelGyro.getGeo!

    console.log 'Map: $scope.mapOptions: geo:', geo

    states = {isDistVincenty: "no"}
    $scope <<< {states}

    $scope.mapOptions = 
      center: new google.maps.LatLng geo.lat, geo.lon
      zoom: 14
      mapTypeId: google.maps.MapTypeId.ROADMAP

    is_first_map_center = true
    $scope.$on 'geoAccelGyro:event', (e, data) ->
      #console.log 'got geoAccelGyro:event: data:', data, 'is_first_map_center:', is_first_map_center
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

    $scope.onMapIdle = ->

    $scope.distMarkers = []
    $scope.distVincenty = 0

    $scope.onMapClick = (event, params) ->
      console.log 'event:', event, 'params:', params, 'states:', $scope.states
      if states.isDistVincenty is not 'no'
        distList.setMarker params[0]
        dist_list = distList.getList!

        _remove_objs_from_googlemap $scope.distMarkers

        markers = _add_markers_to_googlemap dist_list, \#0FF
        path_markers = _add_marker_paths_to_googlemap_from_markers dist_list, \#0F8
        $scope.distMarkers = markers ++ path_markers

        dist_vincenty = _calc_dist_vincenty_from_markers dist_list
        $scope.distVincenty = dist_vincenty.toFixed 3

    $scope.onClearDistList = ->
      console.log 'onClearDistList: start'
      distList.clearList!
      _remove_objs_from_googlemap $scope.distMarkers
      $scope.distVincenty = 0

    dist_vincenty_class = 'hide'
    $scope.$watch (-> $scope.states.isDistVincenty), (new_val, orig_val) ->
      console.log 'scope.states.isDistVincenty: new_val:', new_val, 'orig_val:', orig_val
      dist_vincenty_class := if new_val == 'no' then 'hide' else 'show'

    $scope.distVincentyClass = ->
      dist_vincenty_class

    $scope.onMapZoomChanged = (zoom) ->
      console.log 'zoom:', zoom

    _remove_objs_from_googlemap = (objs) ->
      [each_obj.setMap void for each_obj in objs]
      
    _add_markers_to_googlemap = (markers, color) ->
      #input: markers: a list of markers. each marker: {lat, lng}
      #       color: marker color in googlemap
      #output: 
      markers |> map (marker) -> _add_marker_to_googlemap marker, color

    _add_marker_to_googlemap = (data, color) ->
      marker_opts = 
        map: $scope.myMap
        position: new google.maps.LatLng data.latLng.d, data.latLng.e
        fillColor: color
        strokeColor: color

      new google.maps.Marker marker_opts

    _add_marker_paths_to_googlemap_from_markers = (markers, color) ->
      console.log '_add_marker_paths_to_googlemap_from_markers:', markers

      if markers.length < 2 then return []

      the_markers = markers[0 to -2]
      next_markers = markers[1 to -1]

      idx_list = [0 to the_markers.length - 1]
      marker_list = [{the_marker: the_markers[idx], next_marker: next_markers[idx]} for idx in idx_list]
      marker_list |> map (x) -> _add_marker_path_to_googlemap x, color

    _add_marker_path_to_googlemap = (data, color) ->
      console.log 'data:', data
      current_coord = [data.the_marker.latLng.e, data.the_marker.latLng.d]
      next_coord = [data.next_marker.latLng.e, data.next_marker.latLng.d]
      polyline_opts = 
        map: $scope.myMap
        path: _parse_path [current_coord, next_coord]
        fillColor: color
        strokeColor: color

      new google.maps.Polyline polyline_opts

    _calc_dist_vincenty_from_markers = (markers) ->
      if markers.length < 2 then return 0

      the_markers = markers[0 to -2]
      next_markers = markers[1 to -1]
      idx_list = [0 to the_markers.length - 1]
      marker_list = [{the_marker: the_markers[idx], next_marker: next_markers[idx]} for idx in idx_list]
      dist_list = marker_list |> map (marker_pair) -> distVincenty.distVincenty marker_pair.the_marker.latLng.d, marker_pair.the_marker.latLng.e, marker_pair.next_marker.latLng.d, marker_pair.next_marker.latLng.e
      console.log 'dist_list:', dist_list

      dist_list |> fold1 (+)

    _parse_markers = (the_data_values) ->
      #console.log 'parse_markers: the_data_values:', the_data_values
      results = [_parse_marker each_value for each_value in the_data_values]
      results = [val for val in results when val is not void]

    _parse_marker = (value) ->
      #console.log '_parse_marker: value', value
      geo = value.geo
      if geo is void
        return void

      color = COLOR_MAP[value.the_category]

      markers = [_parse_each_marker(each_geo, color) for each_geo in geo]

      [_add_map_listener each_marker, value for each_marker in markers]

      markers

    _add_map_listener = (marker, value) ->
      #google.maps.event.addListener polygon, 'click', (_show_info value)

    _parse_each_marker = (geo, color) ->
      the_type = geo.type
      the_coordinates = geo.coordinates

      #console.log 'geo:', geo, 'the_type:', the_type, 'the_coordinates', the_coordinates
      switch the_type
      | 'Polygon'    => _parse_polygon the_coordinates, color
      | 'LineString' => _parse_line_string the_coordinates, color
      | 'Point'      => _parse_point the_coordinates, color

    _parse_polygon = (coordinates, color) ->
      polygon_opts = 
        map: $scope.myMap,
        paths: [_parse_path(coord) for coord in coordinates]
        fillColor: color
        strokeColor: color

      #console.log 'polygon_opts:', polygon_opts

      polygon = new google.maps.Polygon polygon_opts

    _parse_line_string = (coordinates, color) ->
      polyline_opts = 
        map: $scope.myMap
        path: _parse_path(coordinates)
        fillColor: color
        strokeColor: color

      polyline = new google.maps.Polyline polyline_opts

    _parse_point = (coordinates, color) ->
      marker_opts = 
        map: $scope.myMap
        position: new google.maps.LatLng coordinates[1], coordinates[0]
        fillColor: color
        strokeColor: color

      #console.log 'marker_opts:', marker_opts

      marker = new google.maps.Marker marker_opts

    _parse_path = (coordinates) ->
      [new google.maps.LatLng coord[1], coord[0] for coord in coordinates]

    #console.log 'MapCtrl: end: scope:', $scope
