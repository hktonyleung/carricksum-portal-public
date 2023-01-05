var copy = '© <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
var url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
//if (typeof osm == 'undefined'){
//    var osm = L.tileLayer(url, { attribution: copy })
//} else {
//    osm = null;
//    delete osm;
//    var osm = L.tileLayer(url, { attribution: copy })
//}

var osm = L.tileLayer(url, { attribution: copy })
document.getElementById('updatemap').innerHTML = "<div id='map'></div>";
var map = L.map('map', { layers: [osm], minZoom: 8 })
/*
map.on('load', function(e) {

    var geojson_branch = JSON.parse($('#geojson_branch').val());
    var geoJSONgroup = L.geoJSON(geojson_branch, {
        onEachFeature: onEachFeature
    }).addTo(map);
    geoJSONgroup.eachLayer(function (layer) {
            map.fitBounds(layer.getBounds());
    });

});
*/
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);
if (typeof $('#geojson_branch').val() === 'undefined' 
|| $('#geojson_branch').val() == ''
|| $('#geojson_branch').val() == 'None' ) {
    createPolygon = true;
} else {
    createPolygon = false;
}

var drawControl = new L.Control.Draw({
    draw: {        
        polygon: createPolygon,
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



function onEachFeature(feature, layer) {
    drawnItems.addLayer(layer);
};