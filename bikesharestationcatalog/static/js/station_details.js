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

    // By default the page will show the first image in case JS isn't enabled
    // We'll just hide that image when JS is enabled so the slideshow can work as expected
    if (document.getElementById('non-js-image')) {
        document.getElementById('non-js-image').style.display = 'none';
    }

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

    var weekday = new Array(7);
        weekday[1] = "Monday";
        weekday[2] = "Tuesday";
        weekday[3] = "Wednesday";
        weekday[4] = "Thursday";
        weekday[5] = "Friday";
        weekday[6] = "Saturday";
        weekday[0] = "Sunday";

    var d = new Date();
    var today = weekday[d.getDay()];

    var labels = ['00:00', '00:05', '00:10', '00:15', '00:20', '00:25', '00:30', '00:35', '00:40', '00:45', '00:50', '00:55', '01:00', '01:05', '01:10', '01:15', '01:20', '01:25', '01:30', '01:35', '01:40', '01:45', '01:50', '01:55', '02:00', '02:05', '02:10', '02:15', '02:20', '02:25', '02:30', '02:35', '02:40', '02:45', '02:50', '02:55', '03:00', '03:05', '03:10', '03:15', '03:20', '03:25', '03:30', '03:35', '03:40', '03:45', '03:50', '03:55', '04:00', '04:05', '04:10', '04:15', '04:20', '04:25', '04:30', '04:35', '04:40', '04:45', '04:50', '04:55', '05:00', '05:05', '05:10', '05:15', '05:20', '05:25', '05:30', '05:35', '05:40', '05:45', '05:50', '05:55', '06:00', '06:05', '06:10', '06:15', '06:20', '06:25', '06:30', '06:35', '06:40', '06:45', '06:50', '06:55', '07:00', '07:05', '07:10', '07:15', '07:20', '07:25', '07:30', '07:35', '07:40', '07:45', '07:50', '07:55', '08:00', '08:05', '08:10', '08:15', '08:20', '08:25', '08:30', '08:35', '08:40', '08:45', '08:50', '08:55', '09:00', '09:05', '09:10', '09:15', '09:20', '09:25', '09:30', '09:35', '09:40', '09:45', '09:50', '09:55', '10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40', '10:45', '10:50', '10:55', '11:00', '11:05', '11:10', '11:15', '11:20', '11:25', '11:30', '11:35', '11:40', '11:45', '11:50', '11:55', '12:00', '12:05', '12:10', '12:15', '12:20', '12:25', '12:30', '12:35', '12:40', '12:45', '12:50', '12:55', '13:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45', '13:50', '13:55', '14:00', '14:05', '14:10', '14:15', '14:20', '14:25', '14:30', '14:35', '14:40', '14:45', '14:50', '14:55', '15:00', '15:05', '15:10', '15:15', '15:20', '15:25', '15:30', '15:35', '15:40', '15:45', '15:50', '15:55', '16:00', '16:05', '16:10', '16:15', '16:20', '16:25', '16:30', '16:35', '16:40', '16:45', '16:50', '16:55', '17:00', '17:05', '17:10', '17:15', '17:20', '17:25', '17:30', '17:35', '17:40', '17:45', '17:50', '17:55', '18:00', '18:05', '18:10', '18:15', '18:20', '18:25', '18:30', '18:35', '18:40', '18:45', '18:50', '18:55', '19:00', '19:05', '19:10', '19:15', '19:20', '19:25', '19:30', '19:35', '19:40', '19:45', '19:50', '19:55', '20:00', '20:05', '20:10', '20:15', '20:20', '20:25', '20:30', '20:35', '20:40', '20:45', '20:50', '20:55', '21:00', '21:05', '21:10', '21:15', '21:20', '21:25', '21:30', '21:35', '21:40', '21:45', '21:50', '21:55', '22:00', '22:05', '22:10', '22:15', '22:20', '22:25', '22:30', '22:35', '22:40', '22:45', '22:50', '22:55', '23:00', '23:05', '23:10', '23:15', '23:20', '23:25', '23:30', '23:35', '23:40', '23:45', '23:50', '23:55', '24:00'];
    var time_labels = labels.map(label => moment(label, 'HH:mm'));

    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
        type: 'line',
        steppedLine: true,
        data: {
            labels: time_labels,
            datasets: [{
                data: window.station_averages_json[today]
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        display: false,
                        max: 1
                    },
                    gridLines: {
                        display: false,
                        drawBorder: false
                    }
                }],
                xAxes: [{
                    type: 'time',
                    ticks: {
                        source: 'labels',
                        maxTicksLimit: 12,
                        autoSkip: true
                    },
                    time: {
                        unit: 'hour',
                        displayFormats: {
                          hour: 'HH:mm'
                       },
                        max: moment('24:00', 'HH:mm')
                    },
                    gridLines: {
                        drawBorder: false
                    }
                }]
            },
            elements: {
                line: {
                    tension: 0,
                    backgroundColor: 'rgba(44, 185, 255, 0.1)',
                    borderWidth: 0
                },
                point: {
                    radius: 0
                }
            },
            legend: {
                display: false
            },
            tooltips: {
                enabled: false
            },
            title: {
                display: true,
                text: today
            }
        }
    });
};
