'use strict'

angular.module 'roadpinFrontendApp'
  .factory 'distVincenty', <[]> ++ -> do

    degToRad = (deg) ->
      deg * Math.PI / 360

    distVincenty: (lat1, lon1, lat2, lon2) ->
      console.log 'start: lat1:', lat1, 'lon1:', lon1, 'lat2:', lat2, 'lon2:', lon2
      # WGS-84 ellipsoid params
      a = 6378137
      b = 6356752.3142
      f = 1/298.257223563

      L = degToRad lon2 - lon1
      U1 = Math.atan (1-f) * Math.tan(degToRad lat1)
      U2 = Math.atan (1-f) * Math.tan(degToRad lat2)
      sinU1 = Math.sin U1
      cosU1 = Math.cos U1
      sinU2 = Math.sin U2
      cosU2 = Math.cos U2
  
      lambda = L 
      lambdaP = 0
      iterLimit = 100
      do 
        sinLambda = Math.sin lambda
        cosLambda = Math.cos lambda
        sinSigma = Math.sqrt (cosU2*sinLambda) * (cosU2*sinLambda) + (cosU1*sinU2 - sinU1*cosU2*cosLambda) * (cosU1*sinU2 - sinU1*cosU2*cosLambda)
        if sinSigma == 0 then return 0 # co-incident points
        cosSigma = sinU1*sinU2 + cosU1*cosU2*cosLambda;
        sigma = Math.atan2 sinSigma, cosSigma
        sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
        cosSqAlpha = 1 - sinAlpha*sinAlpha
        cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
        if isNaN cos2SigmaM then cos2SigmaM = 0;  # equatorial line: cosSqAlpha=0 (§6)
        C = f / 16 * cosSqAlpha * (4 + f *(4 - 3 * cosSqAlpha))
        lambdaP = lambda;
        lambda = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM * cos2SigmaM)))
      while Math.abs lambda - lambdaP > 1e-12 and --iterLimit > 0
      if iterLimit==0 then return NaN # formula failed to converge

      uSq = cosSqAlpha * (a * a - b * b) / (b * b)
      A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
      B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
      deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma * (-1 + 2 * cos2SigmaM *cos2SigmaM) - B / 6 * cos2SigmaM * (-3 + 4 * sinSigma * sinSigma) * (-3 + 4 * cos2SigmaM * cos2SigmaM)))
      s = b * A * (sigma - deltaSigma)
  
      s = s.toFixed 3 # round to 1mm precision
      console.log 'result: s:', s
      s = parseFloat(s)
  
      # // note: to return initial/final bearings in addition to distance, use something like:
      # fwdAz = Math.atan2(cosU2*sinLambda,  cosU1*sinU2-sinU1*cosU2*cosLambda)
      # revAz = Math.atan2(cosU1*sinLambda, -sinU1*cosU2+cosU1*sinU2*cosLambda)
      # { distance: s, initialBearing: radToDeg(fwdAz), finalBearing: radToDeg(revAz) }
