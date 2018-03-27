mapboxgl.accessToken = 'pk.eyJ1IjoiaW1hZG0iLCJhIjoiY2plbnJsMDJyMjU0MTMzcGhxcjZlaXZlNyJ9.k2sPip120jugSJaLNs7Xbw';
// TODO: Add mapbox access token to env (include in template and load in this js)

window.onload = function () {
    map = new mapboxgl.Map({
        container: 'map',
        center: window.geojson['features'][0]['geometry']['coordinates'],
        zoom: 17,
        style: 'mapbox://styles/mapbox/streets-v10'
    });

    map.on('load', function () {
        var nav = new mapboxgl.NavigationControl();
        map.addControl(nav, 'top-left');

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
    });

    if (document.querySelector('.slideshow-container') !== null) {
        var slideIndex = 1;
        showSlides(slideIndex);
        document.getElementById('prev').addEventListener('click', prevSlide);
        document.getElementById('next').addEventListener('click', nextSlide);

        function prevSlide(n) {
            showSlides(slideIndex -= 1);
        }

        function nextSlide(n) {
            showSlides(slideIndex += 1);
        }

        function showSlides(n) {
            var i;
            var slides = document.getElementsByClassName("mySlides");
            if (n > slides.length) {
                slideIndex = 1
            }
            if (n < 1) {
                slideIndex = slides.length
            }
            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
            }

            slides[slideIndex - 1].style.display = "block";
        }
    }
};
