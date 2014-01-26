'use strict'

describe 'Service: distList', (not-it) ->

  # load the service's module
  beforeEach module 'roadpinFrontendApp'

  # instantiate service
  distList = {}
  beforeEach inject (_distList_) ->
    distList := _distList_

  describe 'setMarker properly', (not-it) ->
    expect(!!distList).toBe true

    it 'should add one data to the list', (not-it) ->
      params = 
        pixel:
          x: 10
          y: 10

      distList.setMarker params

      the_list = distList.getList!

      expect(the_list.length).toBe 1

    it 'should add one more data to the list', (not-it) ->
      params = 
        pixel:
          x: 100
          y: 10

      distList.setMarker params
      the_list = distList.getList!

      expect(the_list.length).toBe 2

    it 'should remove one data from the list', (not-it) ->
      params = 
        pixel:
          x: 15
          y: 10

      distList.setMarker params
      the_list = distList.getList!

      expect(the_list.length).toBe 1
