'use strict'

angular.module 'roadpinFrontendApp'
  .directive 'appVersion', <[ version ]> ++ (version) -> do
    link: (scope, element, attrs) ->
      element.text 'the version is' + version
