mapboxgl.accessToken = 'pk.eyJ1IjoiaW1hZG0iLCJhIjoiY2plbnJsMDJyMjU0MTMzcGhxcjZlaXZlNyJ9.k2sPip120jugSJaLNs7Xbw';

window.onload = function() {
    var map = new mapboxgl.Map({
        container: 'map',
        center: [-79.3864974, 43.6580617],
        zoom: 13,
        style: 'mapbox://styles/mapbox/streets-v9',
    });
};
