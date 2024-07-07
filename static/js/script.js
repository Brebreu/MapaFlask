var map = L.map('map').setView([-19.7448, -47.9388], 10);

var baseLayers = {
    "Padrão": L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map),
    "Fundo preto": L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: 'Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    }),
    "Satélite sem Filtros": L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    })
};

var limitesAPA = L.layerGroup();
var areaPasto = L.layerGroup();
var car = L.layerGroup();
var centroides = L.layerGroup();
var userMarkers = L.layerGroup().addTo(map);

var overlays = {
    "Limites APA": limitesAPA,
    "Área de Pasto": areaPasto,
    "CAR": car,
    "Centroides": centroides,
    "User Markers": userMarkers
};

L.control.layers(baseLayers, overlays).addTo(map);

function addUserMarker() {
    var latitude = document.getElementById('latitude').value;
    var longitude = document.getElementById('longitude').value;
    if (latitude && longitude) {
        var marker = L.marker([latitude, longitude]).addTo(userMarkers);
        map.setView([latitude, longitude], 13);
    }
}

function loadData(url, layerGroup, style) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            L.geoJSON(JSON.parse(data), { style: style }).addTo(layerGroup);
            console.log(`Data loaded for ${url}`, data);
        })
        .catch(error => {
            console.error(`Failed to load data from ${url}:`, error);
        });
}

// Estilos personalizados para as camadas
var carStyle = {
    color: 'darkgray',
    weight: 2,
    fill: false
};

var areaPastoStyle = {
    color: 'green',
    weight: 1,
    fillColor: 'lightgreen',
    fillOpacity: 0.5
};

var limitesAPAStyle = {
    color: 'orange',
    weight: 3,
    fill: false
};

loadData('/limite_apa', limitesAPA, limitesAPAStyle);
loadData('/area_do_pasto', areaPasto, areaPastoStyle);
loadData('/skimmed_properties', car, carStyle);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var drawControl = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems
    },
    draw: {
        polygon: true,
        polyline: true,
        rectangle: true,
        circle: true,
        marker: true,
        circlemarker: true
    }
});
map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, function (event) {
    var layer = event.layer;
    drawnItems.addLayer(layer);
});

function exportPolygons() {
    var data = drawnItems.toGeoJSON();
    var convertedData = 'text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(data));
    var a = document.createElement('a');
    a.href = 'data:' + convertedData;
    a.download = 'polygons.geojson';
    a.click();
}

function toggleSidebar() {
    const body = document.body;
    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main");
    sidebar.classList.toggle("open");
    if (sidebar.classList.contains("open")) {
        body.classList.remove("closed-sidebar");
        body.classList.add("open-sidebar");
    } else {
        body.classList.remove("open-sidebar");
        body.classList.add("closed-sidebar");
    }
    setTimeout(() => {
        map.invalidateSize(); // Força o Leaflet a redimensionar o mapa corretamente
    }, 500); // Tempo deve ser igual ao da transição
}


// Adicionar marcadores para cada ponto
function addCentroides(data) {
    data.forEach(row => {
        L.circleMarker([row['Centroide_Prop_y'], row['Centroide_Prop_x']], {
            radius: 4,
            color: 'red',
            fill: true,
            fillColor: 'red',
            fillOpacity: 0.6
        }).bindPopup(`
            CÓDIGO_IMOVEL: ${row['CÓDIGO_IMOVEL']}<br>
            NUM_MODULO: ${row['NUM_MODULO']}<br>
            SITUAÇÃO: ${row['SITUAÇÃO']}<br>
            IMÓVEL: ${row['IMÓVEL']}<br>
            CPF DO(S) PROPRIETÁRIO(S): ${row['CPF DO(S) PROPRIETÁRIO(S)']}<br>
            PROPRIETÁRIO(S): ${row['PROPRIETÁRIO']}<br>
            Área total da propriedade (ha): ${row['Área_propriedade (ha)']}<br>
            Área degradada na APA (ha): ${row['Área_degradada_APA (ha)']}<br>
            Degradação total(%): ${(row['% Degradado'] * 100).toFixed(2).replace('.', ',')}%<br>
            Longitude da propriedade: ${row['Centroide_Prop_x']}<br>
            Latitude da propriedade: ${row['Centroide_Prop_y']}
        `).addTo(centroides);
    });
}
