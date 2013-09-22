'use strict'

angular.module 'angularBrunchSeedLivescriptBowerApp'
  .filter 'interpolate', <[version]> ++ (version) ->
    (text) ->
      String(text)replace /\%VERSION\%/mg version
