let latitude;
let longitude;
let map;
let data;

let heatLayer;


function geoJson2data(geojson) {
    return geojson.features.map(function(feature) {
        return [parseFloat(feature.geometry.coordinates[1]), parseFloat(feature.geometry.coordinates[0]), feature.properties.mag];
    });
}

function loadCoordsAndExecuteMain(position) {
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;

    main();
}

function fallbackCordsAndExecuteMain(){
    latitude = 41.9028;
    longitude = 12.4964;

    main();
}

function loadEarthquakeMarkers(){
    data.features.forEach(function(feature) {
        let point = feature.geometry.coordinates;
        let mag = feature.properties.mag;
        if (mag > 3) {
            let color = mag > 6 ? '#000000' : mag > 5 ? '#750098' : mag > 4 ? '#ff2525' : '#ff7723';
            let circle = L.circle([point[1], point[0]], {
                color: color,
                fillColor: color,
                fillOpacity: 0.5,
                radius: mag*1000
            })
            map.addLayer(circle);
            
            circle.bindPopup(`Unlock this feature by purchasing a standard plan`);
        }
    });
}


function loadHeatMap(){
    heatLayer = L.heatLayer(geoJson2data(data), {radius: 50}).addTo(map);                            
}

function load(){
    loadHeatMap();
    loadEarthquakeMarkers();
}

function requestDataAndLoad(){
    fetch(`/api/query/history/earthquake`)
        .then(response => response.json())
        .then(geodata => {
            data = geodata["data"];
            load();
    });
}

function main(){
    map = L.map('map').setView([latitude, longitude], 8);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);
    
    L.Control.Layers.include({_checkDisabledLayers: function (){}});
    requestDataAndLoad();
}

navigator.geolocation.getCurrentPosition(loadCoordsAndExecuteMain, fallbackCordsAndExecuteMain);
