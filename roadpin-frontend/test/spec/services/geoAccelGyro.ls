'use strict'

describe 'Service: geoAccelGyro', () ->

  # load the service's module
  beforeEach module 'RoadpinFrontendApp'

  # instantiate service
  geoAccelGyro = {}
  beforeEach inject (_geoAccelGyro_) ->
    geoAccelGyro := _geoAccelGyro_
