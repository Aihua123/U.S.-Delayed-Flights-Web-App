function findMatches(wordToWatch, airportNames) {
    return airportNames.filter(place => {
        const regex = new RegExp(wordToWatch, 'gi');
        return place.match(regex)
    })
}

function displayMatches() {
    console.log(this.value);

    let matchArray = findMatches(this.value, airportNames);
    let html = matchArray.map(place => {
        return `
        <li>
        <span class="name">${place}</span>
      </li>
        `;
    });

    let suggestions = document.querySelector("#dest");
    suggestions.innerHTML = html;
}


// set up the airline name drop down list
var selector = d3.select("#selDataset");
d3.json("/airlineName").then((names) => {
    names.forEach(n => {
        selector
            .append("option")
            .text(n)
            .property("value", n);
    })
});


// fetch the ariport data
let airportNames = [];

fetch("/airport")
    .then(blob => blob.json())
    .then(data => { data.forEach(d => airportNames.push(d.FullName)) })

console.log(airportNames)

// listen to destination and origin airport fileds
// have to wait few seconds because it takes time to fetch the data
setTimeout(function () {
    let searchInputD = document.querySelector("#destination");
    // let searchInputO = document.querySelector("#origin");
    searchInputD.addEventListener('change', displayMatches);
    searchInputD.addEventListener('keyup', displayMatches);
    // searchInputO.addEventListener('change', displayMatches);
    // searchInputO.addEventListener('keyup', displayMatches)
}, 5000);




