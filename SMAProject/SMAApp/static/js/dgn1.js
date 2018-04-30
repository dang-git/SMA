//var sideNav = document.getElementById("sn");
//var tabs = sideNav.getElementsByClassName("tab")

//for (var i = 0; i < tabs.length; i++) {
//  tabs[i].addEventListener("click", function() {
//    var current = document.getElementsByClassName("active");
//    current[0].className = current[0].className.replace(" active", "");
//    this.className += " active";
//  });
//}

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