$( "#searchButton" ).on( "click", function() {
    console.log("heuy");
    $("#loadingPage").css("display","block");
    $("#loadingKeyword").text($("#id_keyword").val());
  });