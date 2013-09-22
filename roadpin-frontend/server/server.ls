express = require 'express'
sysPath = require 'path'

startServer = (port, path, callback) ->
  console.log 'startServer: path:', path, 'port:', port
  base = ''

  server = express!;

  server.use (request, response, next) ->
    response.header 'Cache-Control', 'no-cache'
    next!

  server.use base, express["static"] path
  server.all "" + base + "/*", (request, response) ->
    response.sendfile sysPath.join path, 'index.html'
  server.listen port, callback
  server

exports <<< {startServer}