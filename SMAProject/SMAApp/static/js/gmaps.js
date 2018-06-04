$(document).ready(function () {
    $.ajax({
        url: '/ajax/get_geocodes/',
        success: function (data) {
            //var obj = JSON.parse(data);
            initMap(data);
        }
    });
});

function initMap(coordinates) {
    console.log("Setting map");
    var mapCoordinates = coordinates //{lat:19.0759837 , long:72.8776559};
    var coorLength = Object.keys(coordinates).length;
    if (coorLength > 0) {
        var markers = [];
        var infowindow = new google.maps.InfoWindow();
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 4
            // center : {
            //     lat: parseFloat(mapCoordinates[0].lat),
            //     lng: parseFloat(mapCoordinates[0].long),
            // } 
        });
        for (var i = 0; i < coorLength; i++) {
            // Set Gmaps Center only if a coordinate has lat lang.
            if ((mapCoordinates[i].lat != null && mapCoordinates[i].long != null) && map.getCenter() == null) {
                map.setCenter({ lat: parseFloat(mapCoordinates[i].lat), lng: parseFloat(mapCoordinates[i].long) });
            }
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(mapCoordinates[i].lat, mapCoordinates[i].long),
                map: map
            });

            marker.content = "Username: " + mapCoordinates[i].user + "<br>Tweet: " + mapCoordinates[i].tweet

            google.maps.event.addListener(marker, 'click', (function (marker, i) {
                return function () {
                    infowindow.setContent(this.content);
                    infowindow.open(map, marker);
                }
            })(marker));
            //   markers.push(marker);
        }
    } else {
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 4,
            center : {
                lat: parseFloat(14.657369),
                lng: parseFloat(121.056246),
            } 
        });
        // $('#map').append('<div id="nomap"><p>No User Location data has been given</p></div>');
    }
    
    //    For marker clustering
    // var markerCluster = new MarkerClusterer(map, markers,
    //     {imagePath: imagePath});

    // var marker = new google.maps.Marker({
    //     position : {
    //         lat: parseFloat(mapCoordinates.lat),
    //         lng: parseFloat(mapCoordinates.long),
    //     },
    //     map : map
    // });
    console.log("Setting map done");
}