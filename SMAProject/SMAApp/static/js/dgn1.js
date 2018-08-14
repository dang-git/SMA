$(document).ready(function(){

    var pathname = window.location.pathname;
    pathname = pathname.replace(/\//g, '');
    

    $('.tab').removeClass("active");
    if(pathname == ''){
        $('.diagnostics').addClass("active");
    }else{
        $('.' + pathname).addClass("active");
    }
    
    addCommaSeparation();
    
    // retain search box value
    var searchValue = window.sessionStorage['search_keyword'];
    
    $('#searchForm').submit(function(){
        window.sessionStorage['search_keyword'] = $("input[name = 'keyword']").val();
    });
    
    if(searchValue == ''){
        $('#id_keyword').val('');
    }else{
        $('#id_keyword').val(window.sessionStorage['search_keyword']);
    }
    
    loadInsightValues();

    // Hide bootstrap alert after 2 seconds if present.
    if($('div.alert').length > 0) {
        $("div.alert").fadeTo(2000, 500).slideUp(500, function () {
            $("div.alert").slideUp(500);
        });
    }

   // $('.profile-image').on('error' ,function(){
   //     $(this).attr('src', 'https://vignette.wikia.nocookie.net/citrus/images/6/60/No_Image_Available.png/revision/latest?cb=20170129011325')
   // });
})

// display loading screen on search
$( "#searchButton, #searchAgainButton" ).on( "click", function(event) {
    // if searchbox is not empty
    if ($('#id_keyword').val().length > 0) {
        $("#loadingPage").css("display","block");
        $(".load-tweet-text").css("display","block");
        $("#loadingKeyword").text($("#id_keyword").val());
    }
    console.log(event.target.id);
    window.sessionStorage.clear();
  });

function displayLoadingScreen(){
    
}

// Adds commas to digit values
function addCommaSeparation(){
    $('.commaSeparation').each(function(){
        var comma = $(this).text();
        var parts = comma.toString().split(".");
        parts[0] = parts[0].replace(/\D/g, '').replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        comma = parts.join(".");
        $(this).text(comma);
    });
}


// Checks every input box with "search-insights-input" class
// and returns their values if they have data saved on session by using inputId
function loadInsightValues(){
    $("input").each(function(){
        var inputId = $(this).attr('id');
        var inputClass = $(this).attr('class');
        if(inputClass == "search-insights-input" &&
           window.sessionStorage[inputId] != null){
            $(this).val(window.sessionStorage[inputId]);
        }
    });
}

// Unused
// function displayLoadingScreen(){
//         $.ajax({
//             url: '/ajax/get_tweets_count/',
//             success: function (data) {
//             //var obj = JSON.parse(data);
//             updateCount(data);
//             }
//         });
// }


// Saves insights to session
$('.search-insights-input').on('change', function(){
    var insight = $(this).attr('id');
    window.sessionStorage[insight] = $(this).val();
});

function numberFollowersImageError(index){
    $('#number-followers-image' + index).attr('src', profileImage);
}

function engagementGainedImageError(index){
    $('#engagement-gained-image' + index).attr('src', profileImage);
}

function influentialPostImageError(index){
    $('#influential-post-image' + index).attr('src', profileImage);
}


// D3 chart stuff

function resizeTimeline(){

    var width = $('#linechart_container').width();
    var height = $('#linechart_container').height();
    // d3.select('#linechart_container').select('svg').remove();
    nv.addGraph(function() {
        d3.select('#linechart_container').select('svg').remove();
        // d3.select('#linechart_container').select('svg').remove();
    var chart = nv.models.lineChart();

    chart.margin({top: 30, right: 60, bottom: 20, left: 60});

    // width = width - 60 - 60;
    // height = height - 30 - 20;

    var datum = data_linechart_container;

    chart.color(d3.scale.category20().range());


            chart.xAxis
            .tickFormat(function(d) { return d3.time.format('%b-%d %H:%m')(new Date(parseInt(d))) }
);
        chart.yAxis
            .tickFormat(d3.format(',.02f'));



      chart.showLegend(true);

    // chart.height(height);



        // d3.select('#linechart_container svg')
        // // .append("g")
        // .attr("width", '100%')
        // .attr("height", '100%')
        // .attr('viewBox','0 0 '+width+' '+height)
        // .attr('preserveAspectRatio','xMinYMin meet')
        // // .attr("transform", "translate(" + 0 + "," + 0 + ")")
        // .datum(datum)
        // .transition().duration(500)
        // .call(chart);

        d3.select('#linechart_container')
        .append('svg')
        .attr("width", '100%')
        .attr("height", 400)
        .attr('viewbox','0 0 '+ width +' '+ height)
        // .attr('preserveAspectRatio','xMinYMid meet')
        .datum(datum)
        .transition().duration(500)
        .call(chart);
        // nv.utils.windowResize(chart.update);
         

    });

}

window.addEventListener("resize", resizeCharts);

function resizeSource(){

    var width = $('#source_piechart_container').width();
    var height = $('#source_piechart_container').height();

    // data_source_piechart_container=[{"values": [{"label": "Web Client", "value": 32}, {"label": "Android", "value": 240}, {"label": "iPhone", "value": 69}, {"label": "Others", "value": 87}], "key": [32, 240, 69, 87]}];
    d3.select('#source_piechart_container').select('svg').remove();

    nv.addGraph(function() {
        
        d3.select('#source_piechart_container').select('svg').remove();

        var chart = nv.models.pieChart();
        chart.margin({top: 30, right: 60, bottom:20, left: 60});
        var datum = data_source_piechart_container[0].values;

        chart.color(d3.scale.category20().range());
    chart.tooltipContent(function(key, y, e, graph) {
          var x = String(key);
              var y =  String(y) ;

              tooltip_str = '<center><b>'+x+'</b></center>' + y;
              return tooltip_str;
              });
        chart.showLabels(true);

            chart.donut(true);
            chart.donutRatio(0.5);

    chart.showLegend(true);

            chart.labelType("percent");

            // width = width - 60 - 60;
            // height = height - 30 - 20;


        chart
            .x(function(d) { return d.label })
            .y(function(d) { return d.value });


        // chart.height(450);

            d3.select('#source_piechart_container')
            .append('svg')
            .datum(datum)
            .attr("width", '100%')
            .attr("height", 400)
            .attr('viewbox','0 0 '+ width +' '+height)
            .attr('preserveAspectRatio','xMinYMin meet')
            // .attr("transform", "translate(" + Math.min(width,height) / 2 + "," + Math.min(width,height) / 2 + ")")
            .call(chart);

        //     var sasa = nv.utils.windowResize(chart.update);
        // console.log("colors" + sasa);  
        });  
        
        
}

function resizeComposition(){
    


    var width = $('#composition_piechart_container').width();
    var height = $('#composition_piechart_container').height();

    // data_source_piechart_container=[{"values": [{"label": "Web Client", "value": 32}, {"label": "Android", "value": 240}, {"label": "iPhone", "value": 69}, {"label": "Others", "value": 87}], "key": [32, 240, 69, 87]}];

    d3.select('#composition_piechart_container').select('svg').remove();
    nv.addGraph(function() {

        d3.select('#composition_piechart_container').select('svg').remove();
        
        var chart = nv.models.pieChart();
        chart.margin({top: 30, right: 60, bottom:20, left: 60});
        var datum = data_composition_piechart_container[0].values;

        chart.color(d3.scale.category20().range());
    chart.tooltipContent(function(key, y, e, graph) {
          var x = String(key);
              var y =  String(y) ;

              tooltip_str = '<center><b>'+x+'</b></center>' + y;
              return tooltip_str;
              });
        chart.showLabels(true);

            chart.donut(true);
            chart.donutRatio(0.5);

    chart.showLegend(true);

            chart.labelType("percent");

            // width = width - 60 - 60;
            // height = height - 30 - 20;


        chart
            .x(function(d) { return d.label })
            .y(function(d) { return d.value });


        // chart.height(450);


            d3.select('#composition_piechart_container')
            .append('svg')
            .datum(datum)
            .attr("width", '100%')
            .attr("height", 400)
            .attr('viewBox','0 0 '+ width +' '+ height)
            .attr('preserveAspectRatio','xMinYMin meet')
            // .attr("transform", "translate(" + Math.min(width,height) / 2 + "," + Math.min(width,height) / 2 + ")")
            .call(chart);
        });
}


// typeof $('#container') != null --> checks if an element with this id exists

// var resizeAllCharts = debounce(function() {
//     resizeCharts();
// }, 250);

function resizeCharts(){
    var lineChart = document.getElementById('linechart_container');
    var sourceChart = document.getElementById('source_piechart_container');
    var compositionChart = document.getElementById('composition_piechart_container');
    if(lineChart != null) {
        resizeTimeline();
    }

    if(sourceChart != null) {
        resizeSource();
    
    if(compositionChart!= null) {
        resizeComposition();
    }
        
    // resizePolarity();
    // if(typeof $('#multibarhorizontalchart_container') != null){
        // resizeHashtagChart();
    // }
}
}

function resizePolarity(){

    var width = $('#polarity_piechart_container').width();
    var height = $('#polarity_piechart_container').height();

    // data_source_piechart_container=[{"values": [{"label": "Web Client", "value": 32}, {"label": "Android", "value": 240}, {"label": "iPhone", "value": 69}, {"label": "Others", "value": 87}], "key": [32, 240, 69, 87]}];

    nv.addGraph(function() {

        d3.select('#polarity_piechart_container').select('svg').remove();
        
        var chart = nv.models.pieChart();
        chart.margin({top: 30, right: 60, bottom:20, left: 60});
        var datum = data_polarity_piechart_container[0].values;

        chart.color(d3.scale.category20().range());
    chart.tooltipContent(function(key, y, e, graph) {
          var x = String(key);
              var y =  String(y) ;

              tooltip_str = '<center><b>'+x+'</b></center>' + y;
              return tooltip_str;
              });
        chart.showLabels(true);

            chart.donut(true);
            chart.donutRatio(0.5);

    chart.showLegend(true);

            chart.labelType("percent");

            // width = width - 60 - 60;
            // height = height - 30 - 20;


        chart
            .x(function(d) { return d.label })
            .y(function(d) { return d.value });


        // chart.height(450);


            d3.select('#polarity_piechart_container')
            .append('svg')
            .datum(datum)
            .attr("width", '500')
            .attr("height", '500')
            .attr('viewBox','0 0 '+ Math.min(width,height) +' '+Math.min(width,height))
            .attr('preserveAspectRatio','xMinYMin meet')
            // .attr("transform", "translate(" + Math.min(width,height) / 2 + "," + Math.min(width,height) / 2 + ")")
            .call(chart);
        });
}

// Used by save snapshot to keep csrf token safe
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function saveSnapshot(){
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    // var snapshotName = $('#snapshotName').val();
    var send_data = {
        snapshotName :  $('#snapshotName').val(),
        insights : []
    }
    // var snapshotName = $('#snapshotName').val();
    for (var i = 0; i< sessionStorage.length; i++) {
        // -1 is returned by indexOf if there are no words that contains "Insight"
        if(sessionStorage.key(i).indexOf("Insight") != -1){
            send_data.insights.push({
                "insight_container" : sessionStorage.key(i),
                "insight_value" : sessionStorage.getItem(sessionStorage.key(i))
            });
        }
    }
    $.ajax({
        beforeSend: function (xhr, settings) {
            $("#loadingPage").css("display","block");
            $(".saving-snapshot-text").css("display","block");
            if(!csrfSafeMethod(settings.type) && !this.crossDomain){
                xhr.setRequestHeader("X-CSRFToken",csrftoken);
            }
        },
        type: 'POST',
        url: '/ajax/save_snapshot/',
        data: { 'send_data': JSON.stringify(send_data)   //snapshotName : $('#snapshotName').val(), 
               // insight : insights
         },
        // contentType: 'application/json',
        async: false,
        dataType: 'json',
        complete: console.log("naipasa na"),
        success: function(xhr) {
            // alert("At success")
            // if (data == "Saved") {
                // alert("An success occured: " + xhr.status + "," + xhr.statusText + ","+ xhr.readyState);
                if(xhr.status == 200 || xhr.status == 0){
                    $(".saving-snapshot-text").css("display", "none");
                    alert("An success inside occured: " + xhr.status + "," + xhr.statusText + ","+ xhr.readyState);
                    $("#loadingPage").css("display","none");
                    // $("#savingStatus").text(data);
                    $('#saveSnapshotModal').modal('toggle');
                    location.href = "/diagnostics/";
                }
            // }
        },
        error: function(xhr){
            // alert("An error occured: " + xhr.status + "," + xhr.statusText + ","+ xhr.readyState);
            if(xhr.status == 403){
                $(".saving-snapshot-text").css("display", "none");
                $("#loadingPage").css("display","none");
                $('#saveSnapshotModal').modal('toggle');
                $('#snapshotName').append("<p class='save-warning'>Something went wrong, please contact admin.</p>");
                location.href = "/diagnostics/";
            }
            // alert("An error after occured: " + xhr.status + "," + xhr.statusText + ","+ xhr.readyState);
            // location.href = "/diagnostics/";
            // alert("Saving Failed!");
        }
    });
}

$('#loginbtn').on('click',function() {
   if($('#login_email_id').val() && $('#login_password_id').val()){
       validate_credentials();
   }
});

// Submit login form on enter click
$('#login_password_id').on("keyup", function (event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        $('#loginbtn').click();
    }
})

function validate_credentials(){
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var user_credentials = {
        email :  $('#login_email_id').val(),
        password : $('#login_password_id').val(),
    }

    $.ajax({
        beforeSend: function (xhr, settings) {
            if(!csrfSafeMethod(settings.type) && !this.crossDomain){
                xhr.setRequestHeader("X-CSRFToken",csrftoken);
            }
        },
        type: 'POST',
        url: '/ajax/login_user/',
        data: { 'user_credentials': JSON.stringify(user_credentials)
         },
        // contentType: 'application/json',
        // dataType: 'json',
        success: function (data) {
            console.log(data);
            // $('#loginForm').submit();
            location.href="/diagnostics/"
        },
        error: function(xhr){
                // Unauthorized
                if(xhr.status == 401){
                    if (! $('.login-warning').length > 0) {
                        $('#loginForm').append("<p class='login-warning'>Invalid Credentials</p>");
                    }
                }
                // alert("An error occured: " + xhr.status + "," + xhr.statusText);
                // alert("Login Failed!");
            }
    });
}

$('#logoutBtn').on('click',function() {
    logout_user();
});

$('#registeronSnapbtn').on('click', function() {
   location.href = "/register/"
});

function logout_user(){
    sessionStorage.clear();
    $.ajax({
        url: '/ajax/logout_user/',
        success: function (data) {
            location.href="/"
        }
    });
}
// Checks if snapshot data to save is complete (checks: lda and image as of now)
// else save the snapshot
$('#saveSnapshotBtn').on('click', function (event) {
    event.preventDefault();
    if (!$('#snapshotName').val().length > 0) {
        if (!$('.save-warning').length > 0) {
            $('.modal-body').append("<p class='save-warning'>Please fill up this blank</p>")
        }
    } else if (typeof window.sessionStorage['lda_data'] == "undefined" || window.sessionStorage['lda_data'] == null) {
        if (!$('.save-warning').length > 0) {
            $('.modal-body').append("<p class='save-warning'>Topic Clustering Data is still being generated, please wait</p>");
        }
    } else {
        saveSnapshot();
        location.href = "/diagnostics/"
    }
    // saveSnapshot();
    // if(pathname == 'diagnostics'){
    //     location.reload();
    // } else {
    //     location.href="/diagnostics/"
    // }
});

// Load Snapshot modal's submit button 
$('#loadSnapshotBtn').on('click', function() {
    sessionStorage.clear();
    $('#loadSnapshotForm').submit();
});


// $('#saveSnapshotModal').on('shown.bs.modal', function(){
//     if(window.sessionStorage['lda_data'] == null && window.sessionStorage['wc_image'] == null){
//         $('#saveSnapshotBtn').attr({"disabled":"disabled"});
//     } else {
//         $('#saveSnapshotBtn').removeAttr("disabled");
//     }
// });

// Remove the warning on save modal when it closes.
$('#saveSnapshotModal').on('hide.bs.modal', function(){
    if ($('.save-warning').length > 0) {
        $('.save-warning').remove();
    }
});

// Disable snapshot loading when there are no snapshots available
$('#loadSnapshotModal').on('shown.bs.modal', function () {
    if (!$('#id_snapshotchoices').has('option').length > 0) {
        $('#loadSnapshotBtn').prop("disabled", true);
    } else {
        $('#loadSnapshotBtn').prop("disabled", false);
    }
});