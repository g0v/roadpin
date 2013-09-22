'use strict'

angular.module 'roadpinFrontendApp'
  .filter 'interpolate', <[version]> ++ (version) ->
    (text) ->
      String(text)replace /\%VERSION\%/mg version
