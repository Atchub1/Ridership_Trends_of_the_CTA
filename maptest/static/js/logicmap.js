//function wholeMap (year) {
//create a function to return the color for earthquake magnitude https://leafletjs.com/examples/choropleth/
function getColor(ridership) {
    return ridership > 250000 ? '#ff0008' :
           ridership > 200000  ? '#ff7b00' :
           ridership > 150000  ? '#ffcd03' :
           ridership > 100000  ? '#f2ff00' :
           ridership > 50000   ? '#aaff00' :
           ridership > 0   ? '#26ff00' :
                     '#00ffd0';
}

// Create the createMap function
 function createMap(ridershipLayer) {
   console.log(ridershipLayer);
    
      // Create the tile layer that will be the background of our map
      var light = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: attribution,
        maxZoom: 18,
        id: "mapbox.streets",
        accessToken: API_KEY,
        noWrap: true
        });
      var lLine = omnivore.geojson('static/data/CTA_RailLines.geojson');
      console.log(lLine);
      // Create a baseMaps object to hold the satellite layer
    var baseMaps={
      'Chicago': light
    };
    
      // Create an overlayMaps object to hold the earthquake layer
    var overlayMap = {
      'Lines' : lLine,
      'Ridership' : ridershipLayer
    };
    
      // Create the map object with options
      var map = L.map("map", {
        center: [41.85, -87.65],
        zoom: 10,
        layer: [light, overlayMap]
      });
    
      // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
      L.control.layers(baseMaps, overlayMap, {collapsed: false}).addTo(map);
    
       //create legend https://leafletjs.com/examples/choropleth/
    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {

	var div = L.DomUtil.create('div', 'info legend'),
        ridership = [0, 50000, 100000, 150000, 200000, 250000],
        colors =[],
		labels = [];

	// loop through our density intervals and generate a label with a colored square for each interval
	for (var i = 0; i < ridership.length; i++) {
		div.innerHTML +=
			'<i style="background:' + getColor(ridership[i] + 1) + '"></i> ' +
			ridership[i] + (ridership[i + 1] ? '&ndash;' + ridership[i + 1] + '<br>' : '+');
	}

	return div;
    };

    legend.addTo(map);
    //map.setMaxBounds(  [[-90,-180],   [90,180]]  )
    }
    


// Create the createCircles function
function createCircles(response) {
    // Pull the "earthquakes" property off of response.data
    console.log(response);
    //let features = response.features;
    //console.log(features);
    // Initialize an array to hold circles
    let centers = [];
    // Loop through the earthquake array
    response.forEach(station => {
      // For each earthquake, create a circle and bind a popup with the earthquake's magnitude 
      let location = [station.lat, station.lon];
      //console.log(location);
      //console.log(location); 
      let ridership = station.ridership.toFixed(0);
      let name = station.stations;
      //if(ridership > 0){
      //console.log(mag);
      let center = L.circle(location, {
        fillOpacity: .75,
        color: getColor(ridership),
        fillColor: getColor(ridership),
        //Adjust radius
        radius: ridership/3000})
        //}).addTo(myMap);
        .bindPopup(`<h1> ${name} </h1> <hr> <h3>Total Ridership: ${ridership} </h3>`);
      // Add the center to the centers array
      centers.push(center);
      //};
    });
    //console.log(centers);
    
    // // Create a layer group made from the centers array, pass it into the createMap function
    let ridershipLayer = L.layerGroup(centers);
    createMap(ridershipLayer);
  }

  // Perform an API call to the earthquake API to get earthquake information. Call createCircles when complete
  url = `/years/2018`
  d3.json(url, createCircles);
//} 
  //create a list of years to populate select options
// function init (){
//   var selector2 = d3.select("#selDatasetYear");
//   d3.json("/years").then((years) => {
//     console.log(years)
//     years.forEach((year) => {
//       selector2
//           .append("option")
//           .text(year)
//           .property("value", year);
//     });
//     const firstYear = years[0];
//     wholeMap(firstYear);
//   });
 
// }

//init()