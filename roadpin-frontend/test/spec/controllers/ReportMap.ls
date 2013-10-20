'use strict'

describe 'Controller: ReportMapCtrl', (not-it) ->

  # load the controller's module
  beforeEach module 'roadpinFrontendApp'

  ReportMapCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new!
    ReportMapCtrl := $controller 'ReportMapCtrl', do
      $scope: scope
