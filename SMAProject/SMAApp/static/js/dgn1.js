$(document).ready(function(){
    var pathname = window.location.pathname;
    
    pathname = pathname.replace(/\//g, '');
    
    $('.tab').removeClass("active");
    if(pathname == ''){
        $('.diagnostics').addClass("active")
    }else{
        $('.' + pathname).addClass("active");
    }
    
    addCommaSeparation();
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

