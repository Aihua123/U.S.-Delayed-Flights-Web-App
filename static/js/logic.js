//Leaflet airport map
var map = L.map('map', {
  center: [39.50, -98.30],
  zoom: 4
})

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiY29sb3JhZG95ZXRpIiwiYSI6ImNqdHhic3o3aTJoOGI0M280NzhnNXdtazkifQ.vJo8CkS8WdeRMNv0Z0tkug", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.outdoors",

}).addTo(map);

//add Geojson

function aeroporto(feature,
  marker) {
  marker.bindPopup("<b>"+"Airport Performance Stats" + "</b>" + "</BR>" + "</BR>"
    + "AIRPORT CODE " + feature.properties.ORIGIN_AIRPORT + " " + "</BR>" + feature.properties.CITY + " " + feature.properties.STATE + "</p>"
    + "ONTIME FLIGHTS: " + feature.properties.ONTIME + " &nbsp &nbsp" + feature.properties.ONTIME_PCT + "%" + "</BR>"
    + "DELAYED FLIGHTS: " + feature.properties.DELAY + " &nbsp &nbsp" + feature.properties.DELAY_PCT + "%" +"</BR>"
    + "CANCELLED FLIGHTS: " + feature.properties.CANCELLED + " &nbsp &nbsp" + feature.properties.CANCELLED_PCT + "%" + "</BR>"
    + "DIVERTED FLIGHTS: " + feature.properties.DIVERTED + " &nbsp &nbsp" + feature.properties.DIVERTED_PCT + "%" +"</BR>"

  );

  marker.on('mouseover', function (e) {
    this.openPopup();
  });
  marker.on('mouseout', function (e) {
    this.closePopup();
  });

};

L.geoJson(airports, {
  onEachFeature: aeroporto,
  pointToLayer: function (feature, latlng) {
    if (feature.properties.DELAY_PCT > 19) {
      return L.circleMarker(latlng, {
        radius: feature.properties.SUM / 10000,
        color: "red",
        fillColor: "red",
        fillOpacity: 0.5
      });
    } else if (feature.properties.DELAY_PCT > 15) {
      return L.circleMarker(latlng, {
        radius: feature.properties.SUM / 10000,
        color: "yellow",
        fillColor: "yellow",
        fillOpacity: 0.5
      });
    } else if (feature.properties.DELAY_PCT > 9) {
      return L.circleMarker(latlng, {
        radius: feature.properties.SUM / 10000,
        color: "green",
        fillColor: "green",
        fillOpacity: 0.5
      });
    } else if (feature.properties.DELAY_PCT > 1) {
      return L.circleMarker(latlng, {
        radius: feature.properties.SUM / 10000,
        color: "blue",
        fillColor: "blue",
        fillOpacity: 0.5
      });
    }
  }
}).addTo(map);