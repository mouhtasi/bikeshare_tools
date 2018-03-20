mapboxgl.accessToken = 'pk.eyJ1IjoiaW1hZG0iLCJhIjoiY2plbnJsMDJyMjU0MTMzcGhxcjZlaXZlNyJ9.k2sPip120jugSJaLNs7Xbw';

window.onload = function () {
    map = new mapboxgl.Map({
        container: 'map',
        center: [-79.3864974, 43.6580617],
        zoom: 13,
        style: 'mapbox://styles/mapbox/streets-v10'
    });

    map.on('load', function () {
        var nav = new mapboxgl.NavigationControl();
        map.addControl(nav, 'top-left');

        map.addControl(new mapboxgl.GeolocateControl({
            positionOptions: {
                enableHighAccuracy: true
            },
            trackUserLocation: true
        }));

        map.addLayer(
            {
                "id": "points",
                "type": "symbol",
                'source': {
                    'type': 'geojson',
                    'data': window.geojson
                },
                "layout": {
                    "icon-image": "bicycle-share-15",
                    "icon-allow-overlap": true
                }
            }
        )
    });
};
