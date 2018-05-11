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
})

// display loading screen on search
$( "#searchButton, #searchAgainButton" ).on( "click", function() {
    $("#loadingPage").css("display","block");
    $("#loadingKeyword").text($("#id_keyword").val());
    window.sessionStorage.clear();
  });



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
// and returns their values if they have data saved on session
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

function displayLoadingScreen(){
        $.ajax({
            url: '/ajax/get_tweets_count/',
            success: function (data) {
            //var obj = JSON.parse(data);
            updateCount(data);
            }
        });
}

function updateCount(count){

}

// Saves insights to session
$('.search-insights-input').on('change', function(){
    var insight = $(this).attr('id');
    window.sessionStorage[insight] = $(this).val();
});