$(document).ready(function(){
    if (window.sessionStorage['lda_data'] == null ||
            typeof window.sessionStorage['lda_data'] == "undefined"){
        // generateWCImage();
        generateldaPage();
     }
});

// (window.sessionStorage['wc_image'] == null || typeof window.sessionStorage['wc_image'] == "undefined") &&

function generateWCImage(){
    $.ajax({
        url: '/ajax/get_wordcloud_image/',
        success: function (data) {
        window.sessionStorage['wc_image'] = data;
        
        //var obj = JSON.parse(data);
        // make a notif its done?
        console.log("image done");
        }
    });
}


function generateldaPage(){
    $.ajax({
        beforeSend: showSnackbar("Processing Wordcloud..."),
        url: '/ajax/get_lda_page/',
        success: function (data) {
        //var obj = JSON.parse(data);
        // make a notif its done?
        window.sessionStorage['lda_data'] = data;
        console.log("lda done");
        }
    });
}

function showSnackbar(message){
    console.log("show snacku");
}