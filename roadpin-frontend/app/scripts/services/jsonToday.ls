'use strict'
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
      QueryData = $resource url

      console.log 'constants:', constants

      num_query = constants.NUM_QUERY

      the_data = QueryData.query {num_query}, ->
        the_data_dict = {[each_data.the_id, each_data] for idx, each_data of the_data}
        cached_data.data <<< the_data_dict
        console .log 'cached_data.data:', cached_data.data

      cached_data.data
