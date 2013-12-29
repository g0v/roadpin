'use strict'

angular.module 'roadpinFrontendApp'
  .directive 'camera', <[]> ++ -> do
    restrict: 'ACE'
    link: (scope, elm, attrs, ctrl) ->
      if navigator.getUserMedia 
        console.log 'camera: to getUserMedia'
        navigator.getUserMedia {video: true}, (local-media-stream) ->
          elm[0].src = window.URL.createObjectURL local-media-stream
          console.log 'elm.next():', elm.next()
        , (err) ->
          console.log 'unable to load camera:', err
      else
        console.log 'unable to getUserMedia'
