var copy = '© <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
var url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
var osm = L.tileLayer(url, { attribution: copy })
var map = L.map('map', { layers: [osm], minZoom: 8 })

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);
var drawControl = new L.Control.Draw({
    draw: {
        polygon: true,
        circle: false,
        polyline: false,
        rectangle: false,
        circlemarker: false,
        marker: false
    },
    edit: {
        featureGroup: drawnItems,
        edit: true,
        remove: false,
    }
});

map.addControl(drawControl);

map.locate()
  .on('locationfound', e => map.setView(e.latlng, 16))
  .on('locationerror', () => map.setView([22.302711, 114.177216], 8));

map.on('draw:created', function (e) {
    var type = e.layerType,
        layer = e.layer;
    if (type === 'polygon') {
        // Do polygon specific actions
        var polygon = layer.toGeoJSON()
        var convertedPolygon = JSON.stringify(polygon.geometry);
        $('#geo').val(convertedPolygon);
        drawnItems.addLayer(layer);
    }
});
map.on('draw:edited', function (e) {
    var layers = e.layers;

    layers.eachLayer(function (layer) {
        if (layer instanceof L.Polygon){
            // Do polygon specific actions here
            var polygon = layer.toGeoJSON();
            var convertedPolygon = JSON.stringify(polygon.geometry);
            $('#geo').val(convertedPolygon);
            drawnItems.addLayer(layer);
        }
    });

});


//var selectedFeature = null;
function onEachFeature(feature, layer) {
    drawnItems.addLayer(layer);
}