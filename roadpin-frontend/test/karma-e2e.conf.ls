module.exports = (config) ->
  config.set do
    basePath: '../'
    files: [
      'vendor/scripts/jquery/jquery.js'
      'vendor/scripts/angular/angular.js'
      'vendor/scripts/angular-*/angular-*.js'
      'test/vendor/angular-mocks/angular-mocks.js'
      'test/vendor/angular-ng-scenario/angular-ng-scenario.js'
      '_public/js/app.js'
      '_public/**/*.html'
      '_public/*.html'
      'test/e2e/**/*.ls'
      'test/e2e/*.ls'
    ]
    frameworks: <[ ng-scenario ]>
    exclude: []
    logLevel: config.LOG_DEBUG
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
