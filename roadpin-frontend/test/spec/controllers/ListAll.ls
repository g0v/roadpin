'use strict'

describe 'Controller: ListallCtrl', (not-it) ->

  # load the controller's module
  beforeEach module 'roadpinFrontendApp'

  ListallCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new!
    ListallCtrl := $controller 'ListallCtrl', do
      $scope: scope

  it 'should attach a list of awesomeThings to the scope', ->
    expect(scope.awesomeThings.length).toBe 3
