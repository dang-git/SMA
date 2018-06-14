$(document).ready(function(){
    // initldaCss();
})

    var leftPanel;
    var rightPanel;
    var newSvgHeight;

    window.addEventListener("resize", resizeTopicsContainer);


function initldaCss(){
    $('#ldavis_el84844464070221763284634421').css("min-width","auto");
    $('#ldavis_el84844464070221763284634421-top').css("min-width","568px");
    $('#ldavis_el84844464070221763284634421-lambdaInput').css("float","none");
    }
    
    
    $(window).on('load',function() {
        resizeTopicsContainer()
    });

    var newSvgWidth= Math.min(leftPanel.get(0).getBBox().width,rightPanel.get(0).getBBox().width) + 100
    
     // eq(1) - get 2nd element from svg inside div with lda class
     $('.lda').find('svg').eq(1).attr("id","newId1");
     $('#ldavis_el84844464070221763284634421-bar-freqs').attr("transform", "translate(" + 30 + "," + 500 + ")");
    
    
     document.getElementById("ldavis_el84844464070221763284634421-bar-freqs").setAttribute("transform", "translate(" + 30 + "," + 650 + ")");
    window.addEventListener("resize", resizeLda);
    
    
    
    function resizeTopicsContainer(){
        var ldaSvgWidth = $('.lda').find('svg').eq(1).width()

        if(ldaSvgWidth > window.innerWidth){
           var leftPanel = $('g#ldavis_el84844464070221763284634421-leftpanel')
           var rightPanel = $('g#ldavis_el84844464070221763284634421-bar-freqs')
           var topPanel = $('ldavis_el84844464070221763284634421-top')
           var newSvgHeight = leftPanel.get(0).getBBox().height + 100
                              + rightPanel.get(0).getBBox().height;
           var leftPanelHeight = leftPanel.get(0).getBBox().height + 100
        //    $('ldavis_el84844464070221763284634421-top').css({"width":"50%"});
           $('#ldavis_el84844464070221763284634421-bar-freqs').attr("transform", "translate(" + 30 + "," + leftPanelHeight + ")");
           $('.lda').find('svg').eq(1).attr("height",newSvgHeight);
        } else {
        //    topPanel.css({width:100%});
        // $('ldavis_el84844464070221763284634421-top').css({"width":"50%"});
           $('#ldavis_el84844464070221763284634421-bar-freqs').attr("transform", "translate(" + 650 + "," + 60 + ")");
           $('.lda').find('svg').eq(1).attr("height",780);
        }
    
    }
    
    function setTopicsBodyMinWidth(){
        $('#topicsBody').css({"min-width": +"px"});
    }
    // set min width of  width of left panel 