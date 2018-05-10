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
    
    var searchValue = window.localStorage['search_val'];
    
    $('#searchForm').submit(function(){
        window.localStorage['search_val'] = $("input[name = 'keyword']").val();
    });
    
    if(searchValue == ''){
        $('#id_keyword').val('');
    }else{
        $('#id_keyword').val(window.localStorage['search_val']);
    }
    
})

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





