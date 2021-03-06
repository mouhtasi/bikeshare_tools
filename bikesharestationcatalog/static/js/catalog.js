mapboxgl.accessToken = 'pk.eyJ1IjoiaW1hZG0iLCJhIjoiY2plbnJsMDJyMjU0MTMzcGhxcjZlaXZlNyJ9.k2sPip120jugSJaLNs7Xbw';
// TODO: Add mapbox access token to env (include in template and load in this js)

window.onload = function () {
    document.getElementById('map').style.display = 'block';  // the element is hidden unless JS is enabled
    document.getElementById('station-list').style.display = 'none'; // the element is hidden if JS is enabled

    map = new mapboxgl.Map({
        container: 'map',
        center: [-79.3864974, 43.6580617],
        zoom: 12,
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
                "id": "stations",
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
        );

        // When a click event occurs on a feature in the places layer, open a popup at the
        // location of the feature, with description HTML from its properties.
        map.on('click', 'stations', function (e) {
            var station_details = e.features[0];
            var coordinates = station_details.geometry.coordinates.slice();
            var description = station_details.properties.name;
            description += '<br>Available Bikes: ' + station_details.properties.num_bikes_available;
            description += '<br>Available Docks: ' + station_details.properties.num_docks_available;
            description += '<br><a href="' +
                (window.origin + window.station_detail_url).replace('0', station_details.properties.id) + '">Details</a>';

            // Ensure that if the map is zoomed out such that multiple
            // copies of the feature are visible, the popup appears
            // over the copy being pointed to.
            while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
            }

            new mapboxgl.Popup()
                .setLngLat(coordinates)
                .setHTML(description)
                .addTo(map);
        });

        // Change the cursor to a pointer when the mouse is over the places layer.
        map.on('mouseenter', 'stations', function () {
            map.getCanvas().style.cursor = 'pointer';
        });

        // Change it back to a pointer when it leaves.
        map.on('mouseleave', 'stations', function () {
            map.getCanvas().style.cursor = '';
        });
    });
};
