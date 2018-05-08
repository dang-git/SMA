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
    
    var mapCoordinates = coordinates //{lat:19.0759837 , long:72.8776559};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom : 4,
        center : {
            lat: parseFloat(mapCoordinates[0].lat),
            lng: parseFloat(mapCoordinates[0].long),
        } 
    });

    var coorLength = Object.keys(coordinates).length;
    for (var i = 0; i < coorLength; i++) {  
        var marker = new google.maps.Marker({
          position: new google.maps.LatLng(mapCoordinates[i].lat, mapCoordinates[i].long),
          map: map
        });

        var infowindow = new google.maps.InfoWindow({
            content: "Username: " + mapCoordinates[i].user + "<br>Tweet: " + mapCoordinates[i].tweet
          });
    


        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
            //   infowindow.setContent(mapCoordinates[i][0]);
              infowindow.open(map, marker);
            }
          })(marker, i));
    }
  
    // var marker = new google.maps.Marker({
    //     position : {
    //         lat: parseFloat(mapCoordinates.lat),
    //         lng: parseFloat(mapCoordinates.long),
    //     },
    //     map : map
    // });
}