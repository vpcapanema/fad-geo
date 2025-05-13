const map = L.map("map").setView([-22.5, -48.5], 7);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap contributors"
}).addTo(map);

const geoServerBase = "http://3.131.82.224:8080/geoserver/fad";

// Função para adicionar vetor WFS
function addWFS(layerName, color) {
  const url = `${geoServerBase}/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=fad:${layerName}&outputFormat=application/json`;

  fetch(url)
    .then(res => res.json())
    .then(data => {
      L.geoJSON(data, {
        style: {
          color: color,
          weight: 2
        },
        onEachFeature: function (feature, layer) {
          let popup = "<strong>Atributos:</strong><br>";
          for (let key in feature.properties) {
            popup += `${key}: ${feature.properties[key]}<br>`;
          }
          layer.bindPopup(popup);
        }
      }).addTo(map);
    });
}

// Vetores
addWFS("Favorabilidade_media_normalizada_trechos_geografico", "#1f78b4");
addWFS("Limite_regionais_geografico", "#33a02c");
addWFS("Malha_DER_2024_geografico", "#e31a1c");

// Rasters via WMS
const rasterLayers = [
  "indicador_fav_multicriterio_geografico_1",
  "indicador_favorabilidade_socioeconomica",
  "sensibilidade_indicador_favorabilidade_multicriterio_geografico_1"
];

rasterLayers.forEach(layerName => {
  L.tileLayer.wms(`${geoServerBase}/wms`, {
    layers: `fad:${layerName}`,
    format: "image/png",
    transparent: true,
    attribution: "GeoServer"
  }).addTo(map);
});
