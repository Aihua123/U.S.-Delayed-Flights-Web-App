
d3.json("/airlineName", function(names){
    names.forEach(n => {
        d3.select("#selDataset")
            .append("option")
            .text(n)
            .property("value", n);
    })
});
// for building the delay reason bar chart
function init() {
    let namesStore = []
    d3.json("/airlineName",function(names){
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

init();


function optionChanged2(name) {
    buildCharts(name);
};


function buildCharts(name) {
    let url = `/delayReasons/${name}`
    d3.json(url, function(data) {
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

        Plotly.newPlot('plot3', data, layout);

    })
}


// for search form
d3.select('#filter-btn').on('click', function (e) {
    d3.event.preventDefault();
    console.log("working")
    renderTable()
});

function optionChanged(airline) {
    return airline
};

function renderTable(){ 
    d3.selectAll('td').remove();
    let airline = d3.select('#selDataset').node().value;
    let destAirport = d3.select('#autocomplete1').node().value;
    let originAirport = d3.select('#autocomplete2').node().value;
    let month = d3.select('#month').node().value;
    let url = `/delaySearch/${airline}/${destAirport}/${originAirport}/${month}`
    // let url = `/delayReasons/${name}`
    d3.json(url, function(data){
        console.log(data)

        if (data.length == 0) {
            showMessage()
        } else {
            showTable(data)
        }
    })


}

    function showTable(dataGoHere) {
        let myTable = document.getElementById("searchTable")
        dataGoHere.forEach(d => {
            let mynewTr = document.createElement('tr');
            myTable.appendChild(mynewTr);
            dataToshow = []
            dataToshow.push(d.Performance);
            dataToshow.push(d.TotalFlights);
            dataToshow.forEach(x =>{
                let myTd = document.createElement('td');
                myTd.innerHTML = x;
                mynewTr.appendChild(myTd);
            })
        });
        console.log("done")

};
function showMessage() {
    let myTable = document.getElementById("searchTable")
    let mynewTr = document.createElement('tr');
    myTable.appendChild(mynewTr);
    let myTd = document.createElement('td');
    myTd.innerHTML = "Such Flights did not exists";
    mynewTr.appendChild(myTd);

};
