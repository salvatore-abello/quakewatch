const dropdownItems = document.querySelectorAll('.floating-dropdown-item');
const DEFAULT_SETTINGS = {
    "map": "hexbin",
    "points": true
};

/* Variables */

let latitude;
let longitude;
let map;
let data;
let settings;

let key;

let hexLayer;
let heatLayer;

let start = moment().subtract(29, 'days');
let end = moment();

/* Setting-related functions */

function loadSettings(){
    settings = JSON.parse(localStorage.getItem("settings")) || DEFAULT_SETTINGS
}

function saveSettings(k, v){
    settings[k] = v;
    localStorage.setItem("settings", JSON.stringify(settings));
}

/* Coords-related functions */

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

/* Marker-related functions */

function clearMarkers(){
    map.eachLayer(function (layer) {
        if (layer instanceof L.Circle) {
            map.removeLayer(layer);
        }
    });
}

function loadEarthquakeMarkers(){
    clearMarkers();
    saveSettings("map", "hexbin")
    data.features.forEach(function(feature) {
        let point = feature.geometry.coordinates;
        let mag = feature.properties.mag;
        if (mag > 3) { // Remove all points with magnitude less than 4, there are too many of them
            let color = mag > 6 ? '#000000' : mag > 5 ? '#750098' : mag > 4 ? '#ff2525' : '#ff7723';
            let circle = L.circle([point[1], point[0]], {
                color: color,
                fillColor: color,
                fillOpacity: 0.5,
                radius: mag*1000
            })
            map.addLayer(circle);
            
            circle.bindPopup(`<b>Latitude:</b> ${point[1]}</br><b>Longitude:</b> ${point[0]}</br><b>Magnitude:</b> ${mag}</br><b>Time:</b> ${new Date(feature.properties.time).toLocaleString()}`);
        }
    });
}

/* Hexbin-related functions */

function setupHexLayer(){
    hexLayer = L.hexbinLayer({ radius : 12, opacity: 0.5, duration: 500 })
    hexLayer.colorScale().domain([ 1,500 ]).range(["#e2a8ff", "#5d00ff"]);
    hexLayer.colorScaleExtent([ 1,500 ]);
    hexLayer
        .radiusRange(function(d) {return d.length})
        .lng(function(d) { return d[1]; })
        .lat(function(d) { return d[0]; })
        .radiusValue(function (d) {
            return d.length;
    });

    let conv = geoJson2data(data);
    hexLayer.data(conv);
    hexLayer.addTo(map);
}

function loadHexbinMap(){
    saveSettings("map", "hexbin");
    hexLayer.options.opacity = 0.5;
    hexLayer.redraw();
    clearHeatLayer();
}

/* Heatmap-related functions */

function disableHexbinLayer(){
    if (hexLayer && map.hasLayer(hexLayer)) {
        hexLayer.options.opacity = 0;
        hexLayer.redraw();
    }
}

function loadHeatMap(){
    disableHexbinLayer();
    saveSettings("map", "heat")
    if (!heatLayer || !map.hasLayer(heatLayer)) {
        heatLayer = L.heatLayer(geoJson2data(data), {radius: 35}).addTo(map);                
    }
    
}

function clearHeatLayer(){
    map.eachLayer(function (layer) {
    if (layer instanceof L.HeatLayer) {
        map.removeLayer(layer);
    }});
}

/* Map-related functions */

function loadMap(){
    map = L.map('map').setView([latitude, longitude], 8);

    // https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);
    
    L.Control.Layers.include({_checkDisabledLayers: function (){}});
}

function clearMap(){
    saveSettings("map", "none")
    clearHeatLayer();
    disableHexbinLayer();
}

/* Main functions */

function load(){
    setupHexLayer();
    if(settings.map === "hexbin"){
        loadHexbinMap();
    }else if(settings.map == "heat"){
        loadHeatMap();
    }

    if(settings.points){
        loadEarthquakeMarkers();
    }else{
        flexCheckDefault.checked = true;
    }
}

function requestDataAndLoad(start, end){
    fetch(`/api/query/earthquake?starttime=${start.format('YYYY-MM-DD')}&endtime=${end.format('YYYY-MM-DD')}&key=${key}`)
        .then(response => response.json())
        .then(geodata => {
            data = geodata["data"];
            map.eachLayer(function (layer) {
            if (layer instanceof L.HexbinLayer) {
                map.removeLayer(layer);
            }});
            load();
    });
}

function main(){
    loadSettings();
    loadMap();

    start = moment(settings.start) || moment().subtract(29, 'days');
    end = moment(settings.end) || moment();

    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
        'Today': [moment(), moment()],
        'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
        'Last 7 Days': [moment().subtract(6, 'days'), moment()],
        'Last Month': [moment().subtract(29, 'days'), moment()],
        'Last 3 Months': [moment().subtract(89, 'days'), moment()],
        'Last 5 Months': [moment().subtract(150, 'days'), moment()],
        }
    }, cb);

    rfetch("/api/users/current")
    .then(response => response.json())
    .then(userdata => {
        key = userdata.key.key;
        cb(start, end);
    });

}

function cb(start, end) { // callback
    saveSettings("start", start);
    saveSettings("end", end);
    requestDataAndLoad(start, end);
}

/* Event listeners */

flexCheckDefault.addEventListener('change', (event) => {
    saveSettings("points", !event.target.checked);
    if (event.target.checked) {
        map.eachLayer(function (layer) {
            if (layer instanceof L.Circle) {
                map.removeLayer(layer);
            }
        });
    } else {
        loadEarthquakeMarkers(data);
    }
});

dropdownMenuButton.addEventListener('click', (event) => {
    console.log(event.target);
});

dropdownItems.forEach(function(item) {
    item.addEventListener('click', function(event) {
        event.preventDefault(); 
        let ret = {none: clearMap, hexbin: loadHexbinMap, heatmap: loadHeatMap}[this.dataset.value]();
    });
});

navigator.geolocation.getCurrentPosition(loadCoordsAndExecuteMain, fallbackCordsAndExecuteMain);
