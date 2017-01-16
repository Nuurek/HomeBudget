function drawChart() {
    var container = document.getElementById('visualization');

    var dataset = new vis.DataSet(items);

    var options = {
        start: startDate,
        end: endDate
    };
    var Graph2d = new vis.Graph2d(container, dataset, options);
};

(function($){
    $.getScript(visURL, function() {
        drawChart();
    });
})(jQuery);
