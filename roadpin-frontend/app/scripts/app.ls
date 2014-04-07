# Declare app level module which depends on filters, and services
'use strict'

window.onGoogleReady = ->
  console.log 'onGoogleReady: start'
  angular.bootstrap window.document, <[ roadpinFrontendApp ]>

angular.module 'roadpinFrontendApp' <[ ngRoute ngCookies ngResource ngGrid ui.map ui.event ui.bootstrap ]>
  .config <[ $routeProvider $locationProvider ]> ++ ($routeProvider, $locationProvider, config) ->
    $routeProvider
      .when '/view1' templateUrl: '/views/partial1.html'
      .when '/view2' templateUrl: '/views/partial2.html'
      .when '/view3' templateUrl: '/views/partial3.html'
      .when '/view4' templateUrl: '/views/partial4.html'
      .when '/view5' templateUrl: '/views/partial5.html'
      .when '/view6' templateUrl: '/views/partial7.html'
    # Catch all
    .otherwise redirectTo: '/view4'

    # Without serve side support html5 must be disabled.
    $locationProvider.html5Mode false
