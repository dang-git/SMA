$(document).ready(function () {
    // if(typeof window.sessionStorage['bg_started'] != "undefined"){
    //     isSnapshot
    // }

    // if (typeof window.sessionStorage['wc_image'] == "undefined" || window.sessionStorage['wc_image'] == null) {
    //     $('#wordcloudImageContainer').css("display", "none");
    //     // generateWCImage();
    // } else {
    //     $('#imagePlaceholder').css("display", "none");
    //     $('#wordcloudImage').attr({"src":"data:img/png;base64," + window.sessionStorage['wc_image']})
    // }


    if (window.sessionStorage['lda_data'] == null && window.sessionStorage['isSnapshot'] == 'true') {
        getSnapshotLdadata();
        // checkAndProcessLdadata(JSON.stringify(window.sessionStorage['snapshotLdadata']));
        // generateldaPage();
    }
    // if (window.sessionStorage['bg-started'] != 'Y') {
    //     startBackgroundTasks();
    // }
    //load wordcloud
    // if ((typeof window.sessionStorage['bg_started'] == "undefined" || window.sessionStorage['bg_started'] != 'Y')
    //     || window.sessionStorage['bg_done'] != 'Y') {
    //     sessionStorage.setItem("bg_started", "Y")
    //     // window.sessionStorage['bg_started'] == 'Y';
    //     // generateSentiments();
    // }
    if (typeof window.sessionStorage['search_keyword'] != "undefined") {
        if (window.sessionStorage['isSnapshot'] != 'true' && window.sessionStorage['lda_deployed'] != 'Y') {
            sessionStorage.setItem("lda_deployed", "Y");
            startldaDataPull();
        }
        else if (window.sessionStorage['isSnapshot'] != 'true' &&
            (window.sessionStorage['lda_data'] == null ||
                typeof window.sessionStorage['lda_data'] == "undefined")) {
            generateldaData();
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
            $('#wordcloudImage').attr({"src":"data:img/png;base64," + data})
            //var obj = JSON.parse(data);
            // make a notif its done?
            console.log("image done");
        }
    });
}

// Sends go signal to backend to trigger generating lda data
function startldaDataPull() {
    $.ajax({
        url: '/ajax/get_lda_data/',
        complete: generateldaData
    });
}

// This will check lda data on backend
// it also generate "lda page" if lda data already exists
function generateldaData() {
    toggleSnackbar(true);
    $.ajax({
        beforeSend: function () {
            if (window.sessionStorage['lda_page'] == null 
                && window.sessionStorage['lda_data'] != null) {
                generateldaPage();
            }
        },
        url: '/ajax/check_lda_status/',
        success: function (data) {
            checkAndProcessLdadata(data);
        }
    });
}

// Used when data is loaded from snapshot.
function getSnapshotLdadata() {
    $.ajax({
        url: '/ajax/get_snapshot_lda/',
        success: function (data) {
            window.sessionStorage['lda_data'] = JSON.stringify(data);
            generateldaPage();
        }
    });
}

// Periodically check data for lda from backend every 10 secs.
// calls generateldaData everytime backend doesn't give ldadata as result.
function checkAndProcessLdadata(data) {
    if (data == "False") {
        window.setTimeout(generateldaData, 10000);
        console.log("Getting LDA Again");
    } else {
        window.sessionStorage['lda_data'] = data;
        $('#snackbar.show').text("Finished generating LDA Topic cluster");
        toggleSnackbar(false);
        generateldaPage();
        console.log("lda data done");
    }
}



function generateldaPage() {
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

function toggleSnackbar(visible) {
    var snackbar = $('#snackbar')
    if (visible == true) {
        if (!snackbar.hasClass("show")) {
            snackbar.addClass("show");
        }
    } else {
        $("#snackbar.show").fadeTo(3000, 500).slideUp(500, function () {
            $("#snackbar.show").slideUp(500);
        });
        // snackbar.removeClass("show");
        // snackbar.addClass("hide");
    }
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

function validate_registration_email(){
    if ($('.save-warning').length > 0) {
        $('p').remove(".save-warning");
    }
    var form = $('#registrationForm');
    var emailTextbox = $('#reg_email_id');
    // check if textbox has content
    if(emailTextbox.val()){
        $.ajax({
            // type: 'POST',
            // "data-validate-username-url"
            //  is a custom attribute, you put attributes at html
            url: form.attr("data-validate-email-url"),    
            data: form.serialize(),
            dataType: 'json',
            success: function (data) {
                if(data.is_taken){
                    if (!$('.save-warning').length > 0) {
                        $('#reg_email_id').after("<p class='save-warning'>Email has been taken already</p>");
                    }
                    // alert(data.error_message);
                } else {
                    // alert("not taken")
                }
            }
        });
    }
}

$('#reg_email_id').on('keydown',debounce(validate_registration_email,2000,false));

$('#registerBtn').on('click', function() {
    $('#registrationForm').submit();
})

// Unused
// Enable Setting the number of topics
function appendAddNumberofTopics() {
    var addTopicsDiv = ['<label for="ldavis_el84844464070221763284634421-topic-count" style="font-family: sans-serif; font-size: 14px">',
        'Topic Count:',
        '<span id="ldavis_el84844464070221763284634421-topic-value">',
        '</span>',
        '</label>',
        '<input style="width: 50px" type="text" min="0" max="4" step="1" id="ldavis_el84844464070221763284634421-topic-count">',
        '<button id="execute-topic-count" style="margin-left: 5px"> Set Topic </button>']
    $('#ldavis_el84844464070221763284634421-top').prepend(addTopicsDiv);
}