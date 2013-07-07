template = window.Handlebars.compile ($ '#table-tbody-template' .html!)
Data = window.Backbone.Collection.extend do
  url: 'http://localhost:3456/get_json_today'


data = new Data!

render = ->
  content = do
    data: data.toJSON()
  $ '#table-tbody' .html template content