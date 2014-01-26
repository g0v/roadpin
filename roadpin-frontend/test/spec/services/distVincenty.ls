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

  it 'should be able to calculate distance from lat lon', ->
    lat1 = 25.1
    lon1 = 121.5
    lat2 = 25.1
    lon2 = 121.51

    dist = distVincenty.distVincenty(lat1, lon1, lat2, lon2)
    console.log 'lat1:', lat1, 'lon1:', lon1, 'lat2:', lat2, 'lon2:', lon2, 'dist:', dist
    expect(dist == 543.384).toBe true

    lat1 = 25.099
    lon1 = 121.511
    lat2 = 25.1
    lon2 = 121.511

    dist = distVincenty.distVincenty(lat1, lon1, lat2, lon2)
    console.log 'lat1:', lat1, 'lon1:', lon1, 'lat2:', lat2, 'lon2:', lon2, 'dist:', dist
    expect(dist == 55.313).toBe true
