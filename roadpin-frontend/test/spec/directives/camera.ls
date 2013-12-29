'use strict'

describe 'Directive: camera', (not-it) ->

  # load the directive's module
  beforeEach module 'roadpinFrontendApp'

  scope = {}

  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new!

  it 'should make hidden element visible', inject ($compile) ->
    element = angular.element '<camera></camera>'
    element = $compile(element) scope
    expect(element.text!).toBe 'this is the camera directive'
