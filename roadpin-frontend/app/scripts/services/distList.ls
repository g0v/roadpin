'use strict'

{map, filter, head, sort-with} = require 'prelude-ls'
console.log 'sort_with:', sort-with

THRESHOLD_DIST_SAME_POINT = 15

cache_list = {data: []}

angular.module 'roadpinFrontendApp'
  .factory 'distList', <[]> ++ ->
    # Service logic
    # ...
    diffByPixel = (a, b) ->
      xa = a.pixel.x
      ya = a.pixel.y
      xb = b.pixel.x
      yb = b.pixel.y
      diff_x = xa - xb
      diff_y = ya - yb
      Math.sqrt (diff_x * diff_x + diff_y * diff_y)

    _remove_same_point = (params, the_list) ->
      sortWithDiffByPixel = (x, y) ->
        (diffByPixel x, params) - (diffByPixel y, params)

      if not the_list.data or not the_list.data.length then return false

      min_diff_by_px_data = the_list.data |> sort-with sortWithDiffByPixel |> head

      min_diff_by_px = diffByPixel min_diff_by_px_data, params

      if min_diff_by_px > THRESHOLD_DIST_SAME_POINT then return false

      filterMinDiffByPixelData = (x) ->
        (diffByPixel x, params) > min_diff_by_px
          
      the_list.data = the_list.data |> filter filterMinDiffByPixelData

      true

    # Public API here
    do 
      setMarker: (params) ->
        #the_list: {data: []}
        if not _remove_same_point params, cache_list
          cache_list.data ++= [params]

      getList: ->
        cache_list.data

      clearList: ->
        cache_list.data = []