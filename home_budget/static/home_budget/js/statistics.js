function drawChart() {
    var container = document.getElementById('visualization');

    var dataset = new vis.DataSet(expenses);

    var options = {
        style: 'bar',
        barChart: {width:30, align:'center', sideBySide:true},
        stack: true,
        drawPoints: false,
        dataAxis: {
            icons:true
        },
        legend: {left:{position:"top-left"}},
        start: startDate,
        end: endDate,
        dataAxis: {
            showMinorLabels: false
        }
    };

    var groups = new vis.DataSet();
    groups.add({
        id: 0,
        content: "Potrzebne"
    });
    groups.add({
        id: 1,
        content: "Opcjonalne"
    });
    var Graph2d = new vis.Graph2d(container, dataset, options, groups);
};

(function($){
    $.getScript(visURL, function() {
        drawChart();
    });
})(jQuery);
