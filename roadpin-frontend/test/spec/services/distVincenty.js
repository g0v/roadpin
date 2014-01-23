'use strict';

describe('Service: Distvincenty', function () {

  // load the service's module
  beforeEach(module('RoadpinFrontendApp'));

  // instantiate service
  var Distvincenty;
  beforeEach(inject(function(_Distvincenty_) {
    Distvincenty = _Distvincenty_;
  }));

  it('should do something', function () {
    expect(!!Distvincenty).toBe(true);
  });

});
