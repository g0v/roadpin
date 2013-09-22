'use strict'

describe 'Directive: appVersion', (not-it) ->

  # load the directive's module
  beforeEach module 'angularBrunchSeedLivescriptBowerApp'

  scope = {}
  beforeEach inject ($controller, $rootScope) ->
    scope := $rootScope.$new()

  it 'should make hidden element visible', inject ($compile, _version_) ->
    element = angular.element '<span app-version></span>'
    element = $compile(element) scope
    expect(element.text!).toBe 'the version is0.1'
