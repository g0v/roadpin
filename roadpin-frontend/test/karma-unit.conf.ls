module.exports = (config) ->
  config.set do
    basePath: '../'
    files: [
      'test/vendor/jquery/jquery.js'
      'test/vendor/angular/angular.js'
      'test/vendor/angular-loader/angular-loader.js'
      'test/vendor/angular-resource/angular-resource.js'
      'test/vendor/angular-route/angular-route.js'
      'test/vendor/angular-sanitize/angular-sanitize.js'
      'test/vendor/angular-touch/angular-touch.js'
      'test/vendor/angular-animate/angular-animate.js'
      'test/vendor/angular-cookies/angular-cookies.js'
      'test/vendor/ng-grid/ng-grid.js'
      'test/vendor/angular-mocks/angular-mocks.js'
      '_public/js/app.js'
      '_public/js/angular-ui-utils/modules/event/event.js'
      '_public/js/angular-ui-map/*.js'
      '_public/views/*.html'
      '_public/*.html'
      'test/spec/**/*.ls'
    ]
    frameworks: <[ jasmine ]>
    exclude: []
    logLevel: config.LOG_INFO
    reportSlowerThan: 500
    autoWatch: true
    reporters: <[ progress ]>
    junitReporter: 
      outputFile: 'test/test-results.xml'
    port: 3334
    runnerPort: 9100
    browsers: <[ Chrome ]>
    captureTimeout: 5000
    colors: true
    singleRun: false
    urlRoot: '/__karma/'
    preprocessors: 
      '**/*.html': \html2js
      '**/*.ls': \live
    livePreprocessor: 
      options: 
        bare: true
