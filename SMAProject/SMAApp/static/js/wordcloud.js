$(document).ready(function () {
    $.ajax({
        url: '/ajax/get_wordcloud/',
        success: function (data) {
            //var obj = JSON.parse(data);
            initWordCloud(data);
        }
    });
});

function initWordCloud(words) {
    d3.wordcloud()
        .size([1200, 400])
        .selector('#wordcloud')
        .words(words) // Format should be: [{ text: 'word', size: 5 }, { text: 'cloud', size: 15 }]
        .start();
}
