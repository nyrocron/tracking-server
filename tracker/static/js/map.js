var dataURL;
var trackSource;

function init(url) {
    dataURL = url;
    initializeMap();
    updateMap();
}

function updateMap() {
    jQuery.getJSON(dataURL)
        .done(function(data) {
            $('#status').text('');
            showData(data);
        })
        .fail(function () {
            $('#status').addClass('error').text("Failed to load session data");
        })
        .complete(function() {
            setTimeout(updateMap, 30000);
        });
}

function showData(data) {
    var pointCoords = [];
    jQuery.each(data.points, function(i, point) {
        var coords = ol.proj.transform([point.longitude, point.latitude], 'EPSG:4326', 'EPSG:3857');
        pointCoords.push(coords);
    });

    var features = [];
    if (pointCoords.length > 0) {
        features.push(new ol.Feature({
            geometry: new ol.geom.LineString(pointCoords)
        }));
        features.push(new ol.Feature({
            geometry: new ol.geom.Point(pointCoords[pointCoords.length - 1])
        }));
    }

    // update map
    trackSource.clear();
    trackSource.addFeatures(features);
}

function initializeMap() {
    trackSource = new ol.source.Vector();

    var map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.MapQuest({layer: 'osm'})
            }),
            new ol.layer.Vector({
                source: trackSource
            })
        ],
        view: new ol.View({
            center: ol.proj.transform([8.0, 48.0], 'EPSG:4326', 'EPSG:3857'),
            zoom: 10
        })
    });
}
