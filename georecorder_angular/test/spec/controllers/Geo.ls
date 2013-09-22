'use strict'

describe 'Controller: GeoCtrl', (not-it) ->
  # load the controller's module
  beforeEach module 'angularBrunchSeedLivescriptBowerApp'

  GeoCtrl = {}
  scope = {}
  
  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new!
    GeoCtrl := $controller 'GeoCtrl', do
      $scope: scope

  it 'should attach a list of awesomeThings to the scope', ->
    expect (scope.awesomeThings.length) .toBe 3
