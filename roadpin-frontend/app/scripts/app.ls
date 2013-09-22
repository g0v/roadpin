# Declare app level module which depends on filters, and services
'use strict'

angular.module 'roadpinFrontendApp' <[ ngRoute ngCookies ngResource ]>
  .config <[ $routeProvider $locationProvider ]> ++ ($routeProvider, $locationProvider, config) ->
    $routeProvider
      .when '/view1' templateUrl: '/views/partial1.html'
      .when '/view2' templateUrl: '/views/partial2.html'
      .when '/view3' templateUrl: '/views/partial3.html'
    # Catch all
    .otherwise redirectTo: '/view1'

    # Without serve side support html5 must be disabled.
    $locationProvider.html5Mode false
