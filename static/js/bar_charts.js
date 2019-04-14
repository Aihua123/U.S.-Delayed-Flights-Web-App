

function buildPlot1() {
  var url = "/airlineData";
  d3.json(url, function(response) {
    
    // console.log(response);
    var trace1 = {
      y: response.Total_Number_of_Fligths.map(row => row),
      x: response.Airline.map(row => row),
      text: response.Airline.map(row => row),
      name: "Flight",
      type: "scatter",
      yaxis: 'y2',
      // base = [25500,25600,27700],
      // orientation: "h"
    };

    var trace2 = {
      y: response.Total_Number_of_Planes.map(row => row),
      x: response.Airline.map(row => row),
      text: response.Airline.map(row => row),
      name: "Planes",
      type: "bar",
      // yaxis: 'y2',
      // orientation: "h"

    };

    var data = [trace1,trace2];

    var layout = {
      // title: "AIRLINES WITH TOP FLIGHTS",
      barmode: "group",
      yaxis: {title: 'Number of Planes'},
      legend: {
        x: 0,
        y: 1
      },
      yaxis2: {
        title: 'Number of Flights',
        overlaying: 'y',
        side: 'right'
      },
      margin: {
        l: 100,
        r: 100,
        t: 100,
        b: 200
      }
      
    };

    Plotly.newPlot("plot", data, layout);
  });
}
buildPlot1();

// BUild second plot for avergae delays for airlines

function buildPlot2() {
  var url1 = "/delayFlights";
  d3.json(url1, function(response) {
    
    // console.log(response);
    var trace1 = {
      y: response.Total_arrival_Delay.map(row => row),
      x: response.Airline.map(row => row),
      text: response.Airline.map(row => row),
      name: "Total Delay",
      type: "scatter",
      yaxis: 'y2'
      
    };

    var trace2 = {
      y: response.Avg_arrival_delay.map(row => row),
      x: response.Airline.map(row => row),
      text: response.Airline.map(row => row),
      name: "Average Delay",
      type: "bar"
      

    };

    var data = [trace1,trace2];

    var layout = {
      // title: "AIRLINES DELAYS",
      barmode: "group",
      yaxis: {title: 'Average Delay (min)'},
      showlegend: true,
      legend: {
        x: 0,
        y: 1
      },
      yaxis2: {
        title: 'Total Delay (min)',
        overlaying: 'y',
        side: 'right'
      },
      margin: {
        l: 100,
        r: 100,
        t: 100,
        b: 200
      }
      
    };

    Plotly.newPlot("plot2", data, layout);
 
  });

  
}
buildPlot2();

