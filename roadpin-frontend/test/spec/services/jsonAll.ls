'use strict'

describe 'Service: jsonAll', (not-it) ->

  # load the service's module
  beforeEach module 'roadpinFrontendApp'

  # instantiate service
  jsonAll = {}
  beforeEach inject (_jsonAll_) ->
    jsonAll := _jsonAll_

  it 'should do something', ->
    expect(!!jsonAll).toBe true
