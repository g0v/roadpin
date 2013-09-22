'use strict'

describe 'Filter: interpolate', (not-it) ->

  # load the filter's module
  beforeEach module 'angularBrunchSeedLivescriptBowerApp'
  beforeEach inject ($filter) ->
    interpolate = $filter 'interpolate'

  # initialize a new instance of the filter before each test
  it 'should return %VERSION as 0.1', ->
    
    #expect(interpolate \%VERSION%).toBe ('0.1')

  it 'should pass trivial test', ->
    expect(true) .toBe true
