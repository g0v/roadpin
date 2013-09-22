'use strict'

angular.module 'angularBrunchSeedLivescriptBowerApp'
  .directive 'appVersion', <[ version ]> ++ (version) -> do
    link: (scope, element, attrs) ->
      element.text 'the version is' + version
