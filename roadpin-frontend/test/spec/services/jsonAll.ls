'use strict'

describe 'Service: Jsonall', () ->

  # load the service's module
  beforeEach module 'RoadpinFrontendApp'

  # instantiate service
  Jsonall = {}
  beforeEach inject (_Jsonall_) ->
    Jsonall := _Jsonall_

  it 'should do something', () ->
    expect(!!Jsonall).toBe true
