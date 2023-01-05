const copy = '© <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
const url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const osm = L.tileLayer(url, { attribution: copy })
const map = L.map('map', 
    { layers: [osm], 
      minZoom: 8, 
      fullscreenControl: true, }
  )
map.dragging.disable();
//For Polygon
map.locate()
  .on('locationfound', e => map.setView(e.latlng, 15))
  .on('locationerror', () => map.setView([22.302711, 114.177216], 8))
// …
async function load_polygons() {
    const url = `/api/branches/?in_bbox=${map.getBounds().toBBoxString()}`
    const response = await fetch(url)
    const geojson = await response.json()
    console.log(geojson)
    return geojson
}
async function render_polygons() {
    const polygons = await load_polygons()
    L.geoJSON(polygons.results, {onEachFeature: forEachFeature, style: style}).addTo(map)
}

var style = {
  color: "#008000",
  weight: 2,
  opacity: 0.6
}, 
stroke = {
  color: "#fff",
  weight: 3,
  opacity: 0.4
};

function forEachFeature(feature, layer) {

  var popupContent = "<p>Branches Name: <b>" +
          feature.properties.name + "</b> <p> Branches Description:  <b>" +
          feature.properties.desc + "</b>" ;

  if (feature.properties && feature.properties.popupContent) {
      popupContent += feature.properties.popupContent;
  }
  layer.bindPopup(popupContent);
};

// create popup contents
var customPopup = "<b>Branches: </b><br/>";

// specify popup options 
var customOptions =
    {
    'maxWidth': '400',
    'width': '300',
    'className' : 'popupCustom'
    }

map.on('moveend', render_polygons)

map.on('load', function(e) {
  map.dragging.enable();
});
