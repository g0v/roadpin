// This is a manifest file that'll be compiled into application.js, which will include all the files
// listed below.
//
// Any JavaScript/Coffee file within this directory, lib/assets/javascripts, vendor/assets/javascripts,
// or vendor/assets/javascripts of plugins, if any, can be referenced here using a relative path.
//
// It's not advisable to add code directly here, but if you do, it'll appear at the bottom of the
// the compiled file.
//
// WARNING: THE FIRST BLANK LINE MARKS THE END OF WHAT'S TO BE PROCESSED, ANY BLANK LINE SHOULD
// GO AFTER THE REQUIRES BELOW.
//
//= require jquery
//= require jquery_ujs
//= require_tree .

var road_pin = road_pin || {};

road_pin.welcome = {};

road_pin.welcome.index = function(day) {
  var map;
  var markers = [];
  var marker;
  var infowindow;
  var bounds;
  var AtlTab;
  var CaseRange;
  var CaseLineRange;
  var CasePointRange;
  var CaseRangeLineList = [];
  var CaseRangePointList = [];
  var CaseRangelays =[];
  var InfoWindowlays = [];
  var taipei;

  function initialize() {
    taipei = new google.maps.LatLng(25.08,121.45);
    bounds = new google.maps.LatLngBounds();

    var mapOpts = {
      zoom: 12,
      center: taipei,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
    };

    map = new google.maps.Map(document.getElementById("map_canvas"),
        mapOpts);

    $.get('/road_cases?day=' + day, function(ret) {
      for (var x = 0; x < ret.length; x++) {
        var string = "<table border='1' width='500px'>" +
      "<tr><td>行政區</td><td colspan='3'>" + ret[x]['region'] + "</td></tr>" + 
      "<tr><td>施工地點</td><td colspan='3'>" + ret[x]["location"] + "</td></tr>" +
      "<tr><td>施工範圍</td><td colspan='3'>" + ret[x]["range"] + "</td></tr>" +
      "<tr><td>發包日期</td><td></td><td>施工廠商</td><td>" + ret[x]["ctr_wname"] + "</td></tr>" +
      "<tr><td>施工日期</td><td>" + ret[x]["start_on"] + "~" + ret[x]['end_on'] + "</td><td>施工廠商/單位</td><td>" + ret[x]["ctr_oname"] + "</td></tr>" +
      "<tr><td>案件狀態</td><td colspan='3'>" + ret[x]['human_status']+ "</td></tr>";

        string += "</table>";
        parse_points(ret[x]['dt_result'], string);
      }
      set_map();
    }, 'json');
  }

  function add_listener(marker, lat, lng, contentString) {
    google.maps.event.addListener(marker, 'click', function() {
      if (lat && lng) {
        infowindow = new google.maps.InfoWindow();

        infowindow.setContent(contentString);
        infowindow.setPosition(new google.maps.LatLng(lat,lng));

        infowindow.open(map);

        InfoWindowlays.push(infowindow);
      }
    });
  }

  function set_map() {

    if (bounds)
      map.fitBounds(bounds);
  }

  function parse_points(result, contentString) {
    if (result.length <= 0) return [];

    for (var i=0; i< result.length; i++) {
      var points = result[i];
      var points_length = points['POINTS'].length
      if (points_length <= 0) {
        continue;
      }

      var CaseRangeList = [];
      var CaseRangeLineList = [];
      var marker;
      var pointsValue = points["POINTS"];
      var geotype = points["GEO_TYPE"];
      var lat = pointsValue[0]["P2"];
      var lng = pointsValue[0]["P1"];

      switch (points["GEO_TYPE"]) {
      case "LineString":
        for (var j = 0; j < points_length; j++) {
          CaseRangeLineList.push(new google.maps.LatLng(pointsValue[j]["P2"],pointsValue[j]["P1"]));
          //將點位加到map的範圍內
          bounds.extend(new google.maps.LatLng(pointsValue[j]["P2"],pointsValue[j]["P1"]));
        }
        break;
      case "Polygon":
        for (var j = 0; j < points_length; j++) {
          CaseRangeList.push(new google.maps.LatLng(pointsValue[j]["P2"],pointsValue[j]["P1"]));
          //將點位加到map的範圍內
          bounds.extend(new google.maps.LatLng(pointsValue[j]["P2"],pointsValue[j]["P1"]));
        }
        break;
      case "Point":
        for (var j = 0; j < points_length; j++) {
          marker = new google.maps.Marker({position:new google.maps.LatLng(pointsValue[j]["P2"],pointsValue[j]["P1"])});
          markers.push(marker);
          //將點位加到map的範圍內
          bounds.extend(new google.maps.LatLng(pointsValue[j]["P2"],pointsValue[j]["P1"]));
        }
        break;
      } 
      var CaseRange = new google.maps.Polygon({
        paths: CaseRangeList,
                strokeColor: "#FF0000",
                strokeOpacity: 0.8,
                strokeWeight: 3,
                fillColor: "#FF0000",
                fillOpacity: 0.35
      });
      CaseRange.setMap(map);

      var CaseLineRange = new google.maps.Polyline({
        path: CaseRangeLineList,
                    strokeColor: "#FF0000",
                    strokeOpacity: 1.0,
                    strokeWeight: 2
      });
      CaseLineRange.setMap(map);

      CaseRangelays.push(CaseRange);
      CaseRangelays.push(CaseLineRange);

      if (CaseRange) {
        add_listener(CaseRange, lat, lng, contentString);
      }

      if (CaseLineRange) {
        add_listener(CaseLineRange, lat, lng, contentString);
      }

      if (marker) {
        add_listener(CaseLineRange, lat, lng, contentString);
      }
    }
  }

  initialize();
}


