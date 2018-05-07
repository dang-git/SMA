$(document).ready(function(){
    var pathname = window.location.pathname;
    
    pathname = pathname.replace(/\//g, '');
    
    $('.tab').removeClass("active");
    if(pathname == ''){
        $('.diagnostics').addClass("active")
    }else{
        $('.' + pathname).addClass("active");
    }
}) 

