
    var datum = data_multibarhorizontalchart_container;
    // var datum = data_multibarhorizontalchart_container=[
    //     {"x": "#awesm", "y": 319}, 
    //     {"x": "#smsupermalls", "y": 20}, 
    //     {"x": "#everythingshereatsm", "y": 20}, 
    //     {"x": "#pinoysmiles", "y": 13}, 
    //     {"x": "#nationalsupermomsday2018", "y": 2}];

    var margin = {top: 30, right: 60, bottom: 20, left: 160},
    width = parseInt(d3.select("#hashtagChart").style("width")) - margin.left - margin.right,
    height = parseInt(d3.select("#hashtagChart").style("height")) - margin.top - margin.bottom;

var yScale = d3.scale.ordinal()
    .rangeRoundBands([height, 0], 0.1);

var xScale = d3.scale.linear()
    .range([0, width]);


var formatter = d3.format(',.2f');

var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("left");

var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom")
    .tickFormat(function(d){return formatter(d);});

var svg = d3.select("#hashtagChart")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return "<div><span>Tweets:</span> <span style='color:white'>" + d["count"] + "</span></div>"
            //   "<div><span>Name:</span> <span style='color:white'>" + d.Name + "</span></div>" +
            //  "<div><span>Total Sales:</span> <span style='color:white'>" + "$"+ dollarFormatter(d.total) + "</span></div>";
    })

   svg.call(tip);
   datum = datum.sort(function(a,b) {return a["hashtag"] - b["count"]});
   yScale.domain(datum.map(function(d) { return d["hashtag"]; }));
  xScale.domain([0, d3.max(datum, function(d) { return d["count"]; })]);


    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

  svg.append("g")
      .attr("class", "x axis")
      .call(xAxis)
      .attr("transform", "translate(0," + height + ")")
    .append("text")
      .attr("class", "label")
      .attr("transform", "translate(" + width / 2 + "," + margin.bottom / 1.5 + ")")
      .style("text-anchor", "middle")

  svg.selectAll(".bar")
      .data(datum)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("width", function(d) { return xScale(d["count"]);})
      .attr("y", function(d) { return yScale(d["hashtag"]); })
      .attr("height", yScale.rangeBand())
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide);

// Define responsive behavior
function resize() {
    var width = parseInt(d3.select("#hashtagChart").style("width")) - margin.left - margin.right,
    height = parseInt(d3.select("#hashtagChart").style("height")) - margin.top - margin.bottom;
  
    // Update the range of the scale with new width/height
    xScale.range([0, width]);
    yScale.rangeRoundBands([height, 0], 0.1);
  
    // Update the axis and text with the new scale
    svg.select(".x.axis")
      .call(xAxis)
      .attr("transform", "translate(0," + height + ")")
      .select(".label")
        .attr("transform", "translate(" + width / 2 + "," + margin.bottom / 1.5 + ")");
  
    svg.select(".y.axis")
      .call(yAxis);
  
    // Update the tick marks
    xAxis.ticks(Math.max(width/75, 2));
  
    // Force D3 to recalculate and update the line
    svg.selectAll(".bar")
      .attr("width", function(d) { return xScale(d["count"]); })
      .attr("y", function(d) { return yScale(d["hashtag"]); })
      .attr("height", yScale.rangeBand());
  };

  window.addEventListener("resize", resize);