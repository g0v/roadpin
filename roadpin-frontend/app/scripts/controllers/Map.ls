'use strict'

{map, fold, fold1, mean, join} = require 'prelude-ls'

LEGENDS = <[ road_case dig_point ]>

LEGEND_STRING =
  road_case: \道路維護
  dig_point: \道路挖掘

LEGEND_COLOR =
  road_case: \#840
  dig_point: \#808

GRAY_COLOR = \#AAA

LEGEND_MAP =
  taipei_city_road_case: \road_case
  taipei_city_dig_point: \dig_point
  new_taipei_city_dig_point: \dig_point
  kaohsiung_dig_point: \dig_point

angular.module 'roadpinFrontendApp'
  .controller 'MapCtrl', <[ $scope jsonToday geoAccelGyro distVincenty distList ]> ++ ($scope, jsonToday, geoAccelGyro, distVincenty, distList) ->
    geo = geoAccelGyro.getGeo!

    console.log 'Map: $scope.mapOptions: geo:', geo

    states = {isDistVincenty: "no"}
    states <<< {['is_show_' + legend_type, true] for legend_type in LEGENDS}
    the_legend_color = {[key, val] for key, val of LEGEND_COLOR}
    $scope <<< {states, LEGENDS, LEGEND_STRING, LEGEND_COLOR: the_legend_color, LEGEND_MAP}
    $scope <<< {['markers_' + legend_type, []] for legend_type in LEGENDS}

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

    is_first_map_legend = true
    $scope.$watch '$scope.myMap', ->
      if not is_first_map_legend
        return

      is_first_map_legend := false

      $scope.myMap.controls.[google.maps.ControlPosition.TOP_LEFT].push document.getElementById 'map-legend'

    $scope.$watch (-> Object.keys(jsonToday.getData!).length), ->
      the_data = jsonToday.getData!
      data_road_cases = [val for key, val of the_data when LEGEND_MAP[val.the_category] == \road_case]
      data_dig_points = [val for key, val of the_data when LEGEND_MAP[val.the_category] == \dig_point]

      console.log 'Map: data_road_cases:', data_road_cases, 'data_dig_point:', data_dig_points

      markers_road_case = _parse_markers data_road_cases
      markers_dig_point = _parse_markers data_dig_points
      $scope.markers_road_case = markers_road_case
      $scope.markers_dig_point = markers_dig_point

    $scope.onMapIdle = ->

    $scope.distMarkers = []
    $scope.distVincenty = 0

    $scope.onMapClick = (event, params) ->
      console.log 'event:', event, 'params:', params, 'states:', $scope.states
      if states.isDistVincenty is not 'no'
        distList.setMarker params[0]
        dist_list = distList.getList!

        _remove_markers_from_googlemap $scope.distMarkers

        markers = _add_markers_to_googlemap dist_list, \#0FF
        path_markers = _add_marker_paths_to_googlemap_from_markers dist_list, \#0F8
        $scope.distMarkers = markers ++ path_markers

        dist_vincenty = _calc_dist_vincenty_from_markers dist_list
        $scope.distVincenty = dist_vincenty.toFixed 3

    $scope.onClearDistList = ->
      console.log 'onClearDistList: start'
      distList.clearList!
      _remove_markers_from_googlemap $scope.distMarkers
      $scope.distVincenty = 0

    dist_vincenty_class = 'hide'
    $scope.$watch (-> $scope.states.isDistVincenty), (new_val, orig_val) ->
      console.log 'scope.states.isDistVincenty: new_val:', new_val, 'orig_val:', orig_val
      dist_vincenty_class := if new_val == 'no' then 'hide' else 'show'

    $scope.distVincentyClass = ->
      dist_vincenty_class

    $scope.onMapZoomChanged = (zoom) ->
      console.log 'zoom:', zoom

    $scope.onClickLegend = (legend_type) ->
      console.log 'legend_type:', legend_type
      states['is_show_' + legend_type] = not states['is_show_' + legend_type]
      console.log 'states:', states
      $scope.LEGEND_COLOR[legend_type] = if states['is_show_' + legend_type] then LEGEND_COLOR[legend_type] else GRAY_COLOR
      console.log 'LEGEND_COLOR:', LEGEND_COLOR, '$scope.LEGEND_COLOR:', $scope.LEGEND_COLOR, '$scope.markers:', $scope['markers_' + legend_type]
      markers = $scope['markers_' + legend_type]
      if states['is_show_' + legend_type] then _set_markers_to_googlemap markers else _remove_markers_from_googlemap markers

    _set_markers_to_googlemap = (markers) ->
      markers |> map (marker) -> marker.setMap $scope.myMap

    _remove_markers_from_googlemap = (markers) ->
      markers |> map (marker) -> marker.setMap void
      
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
      results |> fold1 (++)

    _parse_marker = (value) ->
      #console.log '_parse_marker: value', value
      geo = value.geo
      if geo is void
        return void

      color = LEGEND_COLOR[LEGEND_MAP[value.the_category]]

      markers = [_parse_each_marker each_geo, color, value for each_geo in geo]

      [_add_map_listener each_marker for each_marker in markers]

      markers

    info_window = new google.maps.InfoWindow do
      content: 'Hello World'

    #google.maps.event.addListener info_window, 'closeclick', ->
    #  info_window.close!

    _add_map_listener = (marker) ->
      google.maps.event.addListener marker, 'click', (event) ->

        console.log 'map_listener: marker:', marker

        if event is not void
          info_window.setPosition event.latLng
          info_window.open $scope.myMap
          info_window.setContent _parse_content marker._value

    _parse_content = (value) ->
      '<div>' + \
        '<p>' + _parse_content_join_str([value.county_name, value.town_name]) + '</p>' + \
        '<p>' + _parse_content_join_str([value.location, value.range]) + '</p>' + \
        '<p>' + (join '~' [value.beginDate, value.endDate]) + '</p>' + \
        '<p>' + _parse_content_join_str([value.work_institute, value.work_institute2]) + '</p>' + \
      '</div>'

    _parse_content_join_str = (the_list) ->
      the_list = [column for column in the_list when column]
      return join ' / ' the_list

    _parse_each_marker = (geo, color, value) ->
      the_type = geo.type
      the_coordinates = geo.coordinates

      #console.log 'geo:', geo, 'the_type:', the_type, 'the_coordinates', the_coordinates
      switch the_type
      | 'Polygon'    => _parse_polygon the_coordinates, color, value
      | 'LineString' => _parse_line_string the_coordinates, color, value
      | 'Point'      => _parse_point the_coordinates, color, value

    _parse_polygon = (coordinates, color, value) ->
      polygon_opts = 
        map: $scope.myMap,
        paths: [_parse_path coord for coord in coordinates]
        fillColor: color
        strokeColor: color

      #console.log 'polygon_opts:', polygon_opts

      polygon = new google.maps.Polygon polygon_opts
      polygon._value = value
      polygon

    _parse_line_string = (coordinates, color, value) ->
      polyline_opts = 
        map: $scope.myMap
        path: _parse_path coordinates
        fillColor: color
        strokeColor: color

      polyline = new google.maps.Polyline polyline_opts
      polyline._value = value
      polyline

    _parse_point = (coordinates, color, value) ->
      marker_opts = 
        map: $scope.myMap
        position: new google.maps.LatLng coordinates[1], coordinates[0]
        fillColor: color
        strokeColor: color

      #console.log 'marker_opts:', marker_opts

      marker = new google.maps.Marker marker_opts
      marker._value = value
      marker

    _parse_path = (coordinates) ->
      [new google.maps.LatLng coord[1], coord[0] for coord in coordinates]

    _parse_center = (coordinates) ->
      center_lat = mean (coordinates |> map -> it[1])
      center_lon = mean (coordinates |> map -> it[0])

      console.log 'coordinates:', coordinates, 'center_lat:', center_lat, 'center_lon:', center_lon

      {center_lat, center_lon}

    #console.log 'MapCtrl: end: scope:', $scope
