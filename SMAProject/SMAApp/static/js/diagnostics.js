$(document).ready(function(){
    generateWCImage();
    generateldaPage();
});


function generateWCImage(){
    $.ajax({
        url: '/ajax/get_wordcloud_image/',
        success: function (data) {
        //var obj = JSON.parse(data);
        // make a notif its done?
        console.log("image done");
        }
    });
}


function generateldaPage(){
    $.ajax({
        url: '/ajax/get_lda_page/',
        success: function (data) {
        //var obj = JSON.parse(data);
        // make a notif its done?
        window.sessionStorage['lda_data'] = data;
        console.log("lda done");
        }
    });
}