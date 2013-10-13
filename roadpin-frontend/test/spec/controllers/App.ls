'use strict'

describe 'Controller: AppCtrl', (not-it) ->
  # load the controller's module
  beforeEach module 'roadpinFrontendApp'

  AppCtrl = {}
  scope = {}
  
  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new!
    AppCtrl := $controller 'AppCtrl', do
      $scope: scope
