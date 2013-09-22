'use strict'

angular.module 'angularBrunchSeedLivescriptBowerApp'
  .controller 'AppCtrl', <[ $scope $location $resource $rootScope version ]> ++ ($scope, $location, $resource, $rootScope, version) ->
    $scope <<< {version}

    $scope.$watch '$location.path()' (active-nav-id or '/') ->
      $scope <<< {active-nav-id}

    $scope.getClass = (id) ->
      if $scope.active-nav-id is id then 'active' else ''

    $scope.awesomeThings = [
      'Livescript'
      'AngularJS'
      'Karma'
      'Yo'
      'Bower'
    ]
