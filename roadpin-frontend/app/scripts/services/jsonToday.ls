'use strict'
CONFIG = window.roadpinFrontendApp.CONFIG

cached_data = 
  data: {}

is_first = true

angular.module 'roadpinFrontendApp'
  .factory 'jsonToday', <[ $resource ]> ++ ($resource) -> do
    getData: ->
      if not is_first
        return cached_data.data

      is_first := false

      url = 'http://' + CONFIG.BACKEND_HOST + '/get_json_today_by_start_date'
      QueryData = $resource url

      the_data = QueryData.query {}, ->
        cached_data.data <<< the_data
        console .log 'cached_data.data:', cached_data.data
          
      cached_data.data
