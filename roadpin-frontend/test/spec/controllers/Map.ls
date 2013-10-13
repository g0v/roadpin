'use strict'

describe 'Controller: MapCtrl', (not-it) ->
  # load the controller's module
  beforeEach module 'roadpinFrontendApp'

  MapCtrl = {}
  scope = {}
  
  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new!
    MapCtrl := $controller 'MapCtrl', do
      $scope: scope
