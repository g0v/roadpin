(function(){
  var template, Data, data, render;
  template = window.Handlebars.compile($('#table-tbody-template').html());
  Data = window.Backbone.Collection.extend({
    url: 'http://localhost:3456/get_json_today'
  });
  data = new Data();
  render = function(){
    var content;
    content = {
      data: data.toJSON()
    };
    return $('#table-tbody').html(template(content));
  };
}).call(this);
