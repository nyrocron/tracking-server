window.app = {};
var app = window.app;

app.map = null;
app.dataURL = null;
app.trackSource = null;
app.lastPosition = null;
app.lastId = 0;
app.refresh = true;
app.follow = true;

app.lineString = null;
app.lastPositionPoint = null;

app.CenterMapControl = function(opt_options) {
    var options = opt_options || {};
    var button = document.createElement('button');
    button.innerHTML = "O";

    var handleCenterMap = function (e) {
        app.follow = !app.follow;
        if (app.follow)
            app.map.getView().setCenter(app.lastPosition);
    };
    button.addEventListener('click', handleCenterMap, false);
    button.addEventListener('touchstart', handleCenterMap, false);

    var element = document.createElement('div');
    element.className = 'center-map ol-unselectable ol-control';
    element.appendChild(button);

    ol.control.Control.call(this, {
        element: element,
        target: options.target
    });
};
ol.inherits(app.CenterMapControl, ol.control.Control);

app.init = function(url) {
    app.dataURL = url;

    app.initializeMap();
    app.updateMap();
};

app.updateMap = function () {
    jQuery.getJSON(app.dataURL + 'since/' + app.lastId + '/')
        .done(function(data) {
            $('#status').removeClass('error').text('');
            app.showData(data);
            if (!data.active) {
                app.refresh = false;
                $('#status').text("Session has finished");
            }
        })
        .fail(function () {
            $('#status').addClass('error').text("Failed to load session data");
        })
        .complete(function() {
            if (app.refresh)
                setTimeout(app.updateMap, 10000);
        });
};

app.showData = function(data) {
    var pointCoords = [];
    jQuery.each(data.points, function(i, point) {
        var coords = ol.proj.transform([point.longitude, point.latitude], 'EPSG:4326', 'EPSG:3857');
        pointCoords.push(coords);
        app.lastId = point.id;
    });

    if (pointCoords.length == 0)
        return;

    //var features = [];
    //features.push(new ol.Feature({
    //    geometry: new ol.geom.LineString(pointCoords)
    //}));

    if (app.lineString == null) {
        app.lineString = new ol.geom.LineString(pointCoords);
        app.trackSource.addFeature(new ol.Feature({geometry: app.lineString}));
    } else {
        jQuery.each(pointCoords, function(i, coords) {
            app.lineString.appendCoordinate(coords);
        });
    }

    var lastPos = pointCoords[pointCoords.length - 1];
    if (app.follow || app.lastPosition == null)
        app.map.getView().setCenter(lastPos);
    app.lastPosition = lastPos;

    if (app.lastPositionPoint == null) {
        app.lastPositionPoint = new ol.geom.Point(lastPos);
        app.trackSource.addFeature(new ol.Feature({geometry: app.lastPositionPoint}));
    } else {
        app.lastPositionPoint.setCoordinates(lastPos);
    }

    //features.push(new ol.Feature({
    //    geometry: new ol.geom.Point(app.lastPosition)
    //}));

    // update map
    //app.trackSource.clear();
    //app.trackSource.addFeatures(features);
};

app.initializeMap = function() {
    app.trackSource = new ol.source.Vector();

    // styles
    var vectorLayerStyle = [
        new ol.style.Style({
            image: new ol.style.Circle({
                fill: new ol.style.Fill({
                    color: '#ff0000'
                }),
                stroke: new ol.style.Stroke({
                    color: 'rgba(51, 153, 204, 0.8)',
                    width: 3.0
                }),
                radius: 6.0
            }),
            fill: new ol.style.Fill({
                color: 'rgba(255, 0, 0, 0.4)'
            }),
            stroke: new ol.style.Stroke({
                color: '#3399CC',
                width: 4.0
            })
        })
    ];

    // map
    app.map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.XYZ({
                    url: 'http://a.tile.opentopomap.org/{z}/{x}/{y}.png',
                    attributions: [
                        new ol.Attribution({
                            html: 'Kartendaten: © <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>-Mitwirkende, SRTM | ' +
                                  'Kartendarstellung: © <a href="http://opentopomap.org/">OpenTopoMap</a>'
                        })
                    ]
                })
                //source: new ol.source.MapQuest({layer: 'sat'})
            }),
            new ol.layer.Vector({
                source: app.trackSource,
                style: vectorLayerStyle
            })
        ],
        view: new ol.View({
            center: ol.proj.transform([0, 0], 'EPSG:4326', 'EPSG:3857'),
            zoom: 13,
            maxZoom: 16
        }),
        controls: ol.control.defaults().extend([
            new app.CenterMapControl()
        ])
    });

    setMapHeight();
    jQuery(window).resize(debounce(setMapHeight));
};

function debounce(func, timeout) {
   var timeoutID;
   timeout = timeout || 200;
   return function () {
      var scope = this, args = arguments;
      clearTimeout(timeoutID);
      timeoutID = setTimeout(function () {
          func.apply(scope, Array.prototype.slice.call(args));
      }, timeout);
   }
}

function setMapHeight() {
    var mapElement = document.getElementById('map');
    var dy = mapElement.getBoundingClientRect().top + window.pageXOffset;
    $(mapElement).height(window.innerHeight - dy);
    app.map.updateSize();
}
