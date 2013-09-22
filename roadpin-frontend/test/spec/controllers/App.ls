'use strict'

describe 'Controller: AppCtrl', (not-it) ->
  # load the controller's module
  beforeEach module 'angularBrunchSeedLivescriptBowerApp'

  AppCtrl = {}
  scope = {}
  
  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new!
    AppCtrl := $controller 'AppCtrl', do
      $scope: scope

  it 'should attach a list of awesomeThings to the scope', ->
    expect (scope.awesomeThings.length) .toBe 5
