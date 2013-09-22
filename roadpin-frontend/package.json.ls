#!/usr/bin/env lsc -cj
author: 'Chia-liang Kao'
name: 'angular-brunch-seed-livescript'
description: 'AngularJS + Brunch + LiveScript'
version: '0.1.1'
homepage: 'https://github.com/clkao/angular-brunch-seed-livescript'
repository:
  type: 'git'
  url: 'https://github.com/clkao/angular-brunch-seed-livescript'
engines:
  node: '0.8.x'
  npm: '1.1.x'
scripts:
  prepublish: './node_modules/.bin/lsc -c package.json.ls && ./node_modules/.bin/lsc -c bower.json.ls'
  start: './node_modules/.bin/brunch watch --server'
  test: 'karma test/karma.config.js'
dependencies: {}
devDependencies:
  karma: '>=0.8.0'
  'karma-junit-reporter': '>=0.1.x'
  'karma-live-preprocessor': '>=0.1.x'
  LiveScript: '>=1.2.0'
  'prelude-ls': '>=1.0.x'
  brunch: '>=1.5.x'
  'javascript-brunch': '>=1.6.x'
  'LiveScript-brunch': '>=1.6.x'
  'css-brunch': '>=1.6.x'
  'sass-brunch': '>=1.7.x'
  'jade-brunch': '>=1.7.x'
  'static-jade-brunch': '>=1.4.8'
  'auto-reload-brunch': '>=1.6.x'
  'uglify-js-brunch': '>=1.7.x'
  'clean-css-brunch': '>=1.5.x'
  'express': '>= 3.1.0'
