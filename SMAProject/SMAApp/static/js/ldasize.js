$(document).ready(function () {
    // initldaCss();
})

// Run resize after page is done loading to fit lda
$(window).on('load', function () {
    resizeTopicsContainer()
});

var leftPanel;
var rightPanel;
var newSvgHeight;

window.addEventListener("resize", resizeTopicsContainer);


function initldaCss() {
    $('#ldavis_el84844464070221763284634421').css("min-width", "auto");
    $('#ldavis_el84844464070221763284634421-top').css("min-width", "568px");
    $('#ldavis_el84844464070221763284634421-lambdaInput').css("float", "none");
}

// var newSvgWidth= Math.min(leftPanel.get(0).getBBox().width,rightPanel.get(0).getBBox().width) + 100
// window.addEventListener("resize", resizeLda);

// Used to adjust Lda bar chart to go below the scatter chart when window is resized
function resizeTopicsContainer() {
    var ldaSvgWidth = $('.lda').find('svg').eq(1).width()

    // Check if lda width does not exceed the current browser window
    if (ldaSvgWidth > window.innerWidth) {
        var leftPanel = $('g#ldavis_el84844464070221763284634421-leftpanel')
        var rightPanel = $('g#ldavis_el84844464070221763284634421-bar-freqs')
        var topPanel = $('ldavis_el84844464070221763284634421-top')
        var newSvgHeight = leftPanel.get(0).getBBox().height + 100
            + rightPanel.get(0).getBBox().height;
        var leftPanelHeight = leftPanel.get(0).getBBox().height + 100
        //    $('ldavis_el84844464070221763284634421-top').css({"width":"50%"});

        var xPosition = 0;  // Used for lda barchart position
        // iterate over each text element to get the greatest text length
        // then apply it to xPosition
        $('#ldavis_el84844464070221763284634421-bar-freqs').children('text').each(function (index) {
            // remove 1st, 2nd and too long texts from the computation
            //  they are not needed
            if (!(index == 0 || index == 1 || this.getBBox().width > 150)) {
                // Compare and set the bigger number to xPosition
                xPosition = Math.max(xPosition, this.getBBox().width);
            }
        });

        xPosition = xPosition + 30; // 30 is the default xPosition so add that
        $('#ldavis_el84844464070221763284634421-bar-freqs').attr("transform", "translate(" + xPosition + "," + leftPanelHeight + ")");
        // eq(1) - get 2nd element from svg inside the div with lda class
        $('.lda').find('svg').eq(1).attr("height", newSvgHeight);
    } else {
        // $('ldavis_el84844464070221763284634421-top').css({"width":"50%"});
        $('#ldavis_el84844464070221763284634421-bar-freqs').attr("transform", "translate(" + 650 + "," + 60 + ")");
        $('.lda').find('svg').eq(1).attr("height", 780);
    }

}

// set the lda's left panel min width
function setTopicsBodyMinWidth() {
    $('#topicsBody').css({ "min-width": +"px" });
}