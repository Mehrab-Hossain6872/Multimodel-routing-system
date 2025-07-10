const map = L.map('map').setView([52.3770, 4.8838], 15); // Centered on Jordaan, Amsterdam
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

let startMarker = null;
let endMarker = null;
let routeLayers = [];
let clickCount = 0;
let startCoords = null;
let endCoords = null;

const modeColor = {
  walk: 'yellow',
  bike: 'orange',
  car: 'blue',
  transfer: 'gray'
};

function clearRoute() {
  routeLayers.forEach(layer => map.removeLayer(layer));
  routeLayers = [];
  if (startMarker) map.removeLayer(startMarker);
  if (endMarker) map.removeLayer(endMarker);
  document.getElementById('route-info').innerHTML = '';
  clickCount = 0;
  startCoords = null;
  endCoords = null;
}

map.on('click', function(e) {
  if (clickCount === 0) {
    clearRoute();
    startCoords = e.latlng;
    startMarker = L.marker(startCoords, {title: 'Start'}).addTo(map);
    clickCount = 1;
  } else if (clickCount === 1) {
    endCoords = e.latlng;
    endMarker = L.marker(endCoords, {title: 'End'}).addTo(map);
    clickCount = 2;
    getRoute();
  }
});

function getRoute() {
  const url = `http://localhost:8000/route?start_lat=${startCoords.lat}&start_lon=${startCoords.lng}&end_lat=${endCoords.lat}&end_lon=${endCoords.lng}`;
  fetch(url)
    .then(res => res.json())
    .then(data => {
      drawRoute(data.segments);
      document.getElementById('route-info').innerHTML = `Total Time: ${data.total_time} minutes | Total Cost: ${data.total_cost} ৳`;
    })
    .catch(err => {
      console.error('Route fetch error:', err);
      document.getElementById('route-info').innerHTML = 'Error fetching route.';
    });
}

function drawRoute(segments) {
  segments.forEach(segment => {
    const latlngs = segment.coords; // No need to swap
    const color = modeColor[segment.mode] || 'black';
    const polyline = L.polyline(latlngs, {color, weight: 6, opacity: 0.8}).addTo(map);
    routeLayers.push(polyline);
  });
} 