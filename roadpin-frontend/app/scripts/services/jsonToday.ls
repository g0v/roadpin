'use strict'

{initial, last} = require 'prelude-ls'

CONFIG = window.roadpinFrontendApp.CONFIG

cached_data = 
  data: {}

is_first = true

angular.module 'roadpinFrontendApp'
  .factory 'jsonToday', <[ $resource constants ]> ++ ($resource, constants) -> do
    getData: ->
      if not is_first
        return cached_data.data

      is_first := false

      url = 'http://' + CONFIG.BACKEND_HOST + '/get_json_today_by_start_date'
      num_query = constants.NUM_QUERY

      query_success = (the_data, getResponseHeaders) ->
        console.log 'the_data:', the_data, 'getResponseHeaders:', getResponseHeaders!

        new_data = if the_data.length == num_query then initial the_data else the_data

        new_data_dict = {[each_data.the_id, each_data] for each_data in new_data when each_data and each_data.beginDate and each_data.endDate}

        cached_data.data <<< new_data_dict

        if the_data.length == num_query
          last_data = last the_data
          console.log 'last_data:', last_data
          next_id = last_data.json_id

          console.log 'next_id:', next_id, 'last_data:', last_data

          query_data next_id

      query_data = (next_id) ->
          NewQueryData = $resource url
          NewQueryData.query {num_query, next_id}, query_success

      QueryData = $resource url
      QueryData.query {num_query}, query_success

      cached_data.data
