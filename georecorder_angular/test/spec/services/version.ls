'use strict'

describe 'Service: version', (not-it) ->

  # load the service's module
  beforeEach module 'angularBrunchSeedLivescriptBowerApp'

  # instantiate service
  version = {}
  beforeEach inject (_version_) ->
    version := _version_

  it 'should be trivial test', ->
    expect(true).toBe true

  it 'version should be 0.1', ->
    expect(version).toBe 0.1
