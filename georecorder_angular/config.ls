exports.config =
  # See docs at http://brunch.readthedocs.org/en/latest/config.html.
  modules:
    definition: false
    wrapper: (path, data) ->
      """
(function() {
  'use strict';
  #{data}
}).call(this);\n\n
      """
  paths:
    public: '_public'
  files:
    javascripts:
      joinTo:
        'js/app.js': /^app/
        #'js/test.js': /^test/
        'js/vendor.js': /^vendor/
      order:
        before:
          'vendor/scripts/console-helper.js'
          'vendor/scripts/jquery/jquery.js'
          'vendor/scripts/bootstrap-sass/tooltip.js'
          'vendor/scripts/bootstrap-sass/transition.js'
          'vendor/scripts/bootstrap-sass/affix.js'
          'vendor/scripts/bootstrap-sass/alert.js'
          'vendor/scripts/bootstrap-sass/button.js'
          'vendor/scripts/bootstrap-sass/carousel.js'
          'vendor/scripts/bootstrap-sass/collapse.js'
          'vendor/scripts/bootstrap-sass/dropdown.js'
          'vendor/scripts/bootstrap-sass/modal.js'
          'vendor/scripts/bootstrap-sass/scrollspy.js'
          'vendor/scripts/bootstrap-sass/tab.js'
          'vendor/scripts/angular/angular.js'
          'vendor/scripts/angular-animate/angular-animate.js'
          'vendor/scripts/angular-cookies/angular-cookies.js'
          'vendor/scripts/angular-i18n/angular-i18n.js'
          'vendor/scripts/angular-loader/angular-loader.js'
          'vendor/scripts/angular-resource/angular-resource.js'
          'vendor/scripts/angular-route/angular-route.js'
          'vendor/scripts/angular-touch/angular-touch.js'

    stylesheets:
      joinTo:
        'css/app.css': /^(app|vendor)/

    templates:
      joinTo: 'js/templates.js'

  # Enable or disable minifying of result js / css files.
  # minify: true
  server:
    path: 'server/server.ls'


