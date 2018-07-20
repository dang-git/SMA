$(document).ready(function () {
    if(window.sessionStorage['isSnapshot'] == true && snapshotLdadata != null){
        processldaData(JSON.stringify(snapshotLdadata));
    }
    // if (window.sessionStorage['bg-started'] != 'Y') {
    //     startBackgroundTasks();
    // }
    //load wordcloud
    if ((window.sessionStorage['bg_started'] != 'Y' || typeof window.sessionStorage['bg_started'] == "undefined")
        || window.sessionStorage['bg_done'] != 'Y') {
        sessionStorage.setItem("bg_started", "Y")
        // window.sessionStorage['bg_started'] == 'Y';
        // generateSentiments();
    }

    if (window.sessionStorage['lda_deployed'] != 'Y' || typeof window.sessionStorage['bg_started'] == "undefined") {
        sessionStorage.setItem("lda_deployed", "Y");
        // startldaDataPull();
    }

    if (window.sessionStorage['wc_image'] == null ||
        typeof window.sessionStorage['wc_image'] == "undefined") {
        $('#wordcloudImageContainer').css("display", "none");
        generateWCImage();
    } else {
        $('#imagePlaceholder').css("display", "none");
    }

    // load topic clustering
    if (window.sessionStorage['lda_data'] == null ||
        typeof window.sessionStorage['lda_data'] == "undefined") {
        // generateldaData();
        // $('#ldaPage').css("display", "none");
    }
    else if ((window.sessionStorage['lda_data'] != null &&
        (window.sessionStorage['lda_page'] == null ||
            typeof window.sessionStorage['lda_page'] == "undefined"))) {
        generateldaPage();
    }
    else {
        $('#ldaPlaceholder').css("display", "none");
        $('#ldaPage').html(window.sessionStorage['lda_page']);
    }
});

// (window.sessionStorage['wc_image'] == null || typeof window.sessionStorage['wc_image'] == "undefined") &&
var pathname = window.location.pathname;
pathname = pathname.replace(/\//g, '');

function generateWCImage() {
    $.ajax({
        url: '/ajax/get_wordcloud_image/',
        success: function (data) {
            window.sessionStorage['wc_image'] = data;
            if (pathname == "topics") {
                // location.reload();
            }
            $('#imagePlaceholder').css("display", "none");
            $('#wordcloudImageContainer').css("display", "block");
            //var obj = JSON.parse(data);
            // make a notif its done?
            console.log("image done");
        }
    });
}


function startldaDataPull() {
    $.ajax({
        url: '/ajax/get_lda_data/',
        complete: generateldaData
    });
}

function generateldaData() {
    $.ajax({
        beforeSend: function () {
            if (window.sessionStorage['lda_page'] == null 
                && window.sessionStorage['lda_data'] != null) {
                generateldaPage();
            }
        },
        url: '/ajax/check_lda_status/',
        success: function (data) {
            processldaData(data);
        }
    });
}

// Periodically check data for lda from server every 10 secs.
function processldaData(data) {
    if (data == "False") {
        window.setTimeout(generateldaData, 10000);
        console.log("Getting LDA Again");
    } else {
        window.sessionStorage['lda_data'] = data;
        generateldaPage();
        console.log("lda data done");
    }
}



function generateldaPage() {
    console.log("inside lda page");
    $.ajax({
        url: '/ajax/get_lda_page/',
        success: function (data) {
            window.sessionStorage['lda_page'] = data;
            //window.sessionStorage['lda_deployed'] = 'N';
            if (pathname == "topics") {
                if (window.sessionStorage['lda_data'] != null) {
                    $('#ldaPlaceholder').css("display", "none");
                    $('#ldaPage').css("display", "block");
                    $('#ldaPage').html(data);
                }
            }
            console.log("lda page done");
        }
    });
}

function generateSentiments() {
    console.log("inside sentiments");

    $.ajax({
        url: '/ajax/get_sentiments/',
        success: function (data) {
            if(data == "True"){
                sessionStorage.setItem("bg_done", "Y");
                console.log("sentiments done");
            }
        }
    });
}

function startBackgroundTasks() {
    console.log("Starting Background Task");
    $.ajax({
        beforeSend: function () {
            window.sessionStorage['bg-started'] == 'Y';
        },
        url: '/ajax/start_background_tasks/',
        success: function (data) {
            window.sessionStorage['sentiments'] = data;
            //window.sessionStorage['lda_deployed'] = 'N';
            if (pathname == "sentiments") {
                if (window.sessionStorage['sentiments'] != null) {
                    // $('#ldaPlaceholder').css("display", "none");
                    // $('#ldaPage').css("display", "block");
                    // $('#ldaPage').html(data);
                }
            }
            console.log("sentiments done");
        }
    });
}

function validate_email(){
    var form = $('#snapshotForm');
    var emailTextbox = $('#id_email');
    console.log("box " + emailTextbox.val());
    // check if textbox has content
    if(emailTextbox.val()){
        $.ajax({
            // "data-validate-username-url"
            //  is a custom attribute, you put attributes at html
            url: form.attr("data-validate-email-url"),    
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                if(data.is_taken){
                    alert(data.error_message);
                } else {
                    // alert("not taken")
                }
            }
        });
    }
}

$('#id_email').on('keydown',debounce(validate_email,2000,false));



function showSnackbar(message) {
    console.log("show snacku");
}