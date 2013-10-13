'use strict'

describe 'Service: jsonToday', (not-it) ->

  # load the service's module
  beforeEach module 'roadpinFrontendApp'

  # instantiate service
  jsonToday = {}
  beforeEach inject (_jsonToday_) ->
    jsonToday := _jsonToday_

  it 'should do something', ->
    expect(!!jsonToday).toBe true
