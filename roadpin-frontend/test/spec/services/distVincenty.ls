'use strict'

describe 'Service: distVincenty', (not-it) ->

  # load the service's module
  beforeEach module 'roadpinFrontendApp'

  # instantiate service
  distVincenty = {}
  beforeEach inject (_distVincenty_) ->
    distVincenty := _distVincenty_

  it 'should do something', ->
    expect(!!distVincenty).toBe true
