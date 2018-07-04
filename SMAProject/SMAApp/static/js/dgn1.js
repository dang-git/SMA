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
    var searchValue = window.sessionStorage['search_val'];
    
    $('#searchForm').submit(function(){
        window.sessionStorage['search_val'] = $("input[name = 'keyword']").val();
    });
    
    if(searchValue == ''){
        $('#id_keyword').val('');
    }else{
        $('#id_keyword').val(window.sessionStorage['search_val']);
    }
    loadInsightValues();

   // $('.profile-image').on('error' ,function(){
   //     $(this).attr('src', 'https://vignette.wikia.nocookie.net/citrus/images/6/60/No_Image_Available.png/revision/latest?cb=20170129011325')
   // });
})

// display loading screen on search
$( "#searchButton, #searchAgainButton" ).on( "click", function(event) {
    $("#loadingPage").css("display","block");
    $(".load-tweet-text").css("display","block");
    $("#loadingKeyword").text($("#id_keyword").val());
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


$('#searchButton').on('click', function(){
// alert("heyo");
});

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

// Added debounce to improve chart resizing performance
// It delays the function execution
function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};

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
    var insights = [];
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
        dataType: 'json',
        complete: console.log("naipasa na"),
        success: function (data) {
            if (data == "True") {
                $(".saving-snapshot-text").css("display", "block");
                $("#savingStatus").text(data);
            }
        },
        error: function(xhr){
            alert("An error occured: " + xhr.status + " " + xhr.statusText);
    }});
}


