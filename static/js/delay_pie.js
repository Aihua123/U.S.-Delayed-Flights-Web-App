function init() {
    let namesStore = []
    d3.json("/airlineName", function(names){
        names.forEach(n => {
            namesStore.push(n)
            d3.select("#delayReason")
                .append("option")
                .text(n)
                .property("value", n);
        })
        buildCharts(namesStore[0])
    });

}

function optionChanged2(name) {
    buildCharts(name);
};
function buildCharts(name) {
    let url = `/delayReasons/${name}`
    d3.json(url,function(data) {
        console.log(data)
        let values = data.delayFlightsNum
        let labels = data.delayType
        var data = [{
            values: values,
            labels: labels,
            type: 'pie'
        }];

        var layout = {
            height: 400,
            width: 500
        };

        Plotly.newPlot('plot', data, layout);

    })
}

init();

