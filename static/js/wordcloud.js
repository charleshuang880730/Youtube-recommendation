var count = 0;

function uid(name) {
  return new Id("O-" + (name == null ? "" : name + "-") + ++count);
}

function Id(id) {
  this.id = id;
  this.href = new URL(`#${id}`, location) + "";
}

Id.prototype.toString = function() {
  return "url(" + this.href + ")";
};

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

tip = d3.tip().attr('class', 'd3-tip').attr('style', "z-index: 100000;").html(
  d => 
  `
  <div class="tip media text-wrap" style="background-color: white; width: 25rem; border: 3px grey solid;">
    <img src=${d.data.photo} class="align-self-start mr-3">
    <div class="media-body">
      <h5 class="mt-0">${d.data.author}</h5>
      <p>${d.data.name}</p>
    </div>
  </div>
  `
);

chart = (data, btns) => {

  //color = d3.scaleOrdinal(data.map(d => d.group), d3.schemeCategory10)
  //color = d3.scaleOrdinal(data.map(d => d.group), d3.schemeRdYlGn[5])
  color = d3.scaleOrdinal([4,3,2,1,0], d3.schemeRdYlGn[5])
  color_index = {}

  btns.selectAll("button")
      .each(function(){
        var txt = d3.select(this).text();
        var weight = d3.select(this).attr("weight");
        color_index[txt] = weight;
        
        var rgb_item = hexToRgb(color(weight));
        var rgb_color = "rgba("+rgb_item['r']+","+rgb_item['g']+","+rgb_item['b']+",0.7)"
        d3.select(this).attr("style","border-radius: 30px;margin: 8 0;background-color:"+rgb_color);
      })

  const root = pack(data);
  
  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height])
      .attr("font-size", 20)
      .attr("font-family", "sans-serif")
      .attr("text-anchor", "middle")
      .attr("class", "img-fluid")
      .attr("alt", "Responsive image")
      .attr("width", "100%");

      //svg.append("filter").attr("id","shadow").append("feDropShadow").attr("dx", 0.2).attr("dy", 0.4).attr("stdDeviation", 0.1);

  if(data.length == 0)
      return svg.node();
  
  svg.call(tip);

  const leaf = svg.selectAll("g")
    .data(root.leaves(), d => d)
    .join("g")
      .attr("transform", d => `translate(${d.x + 1},${d.y + 1})`)
      .attr("class", d => `bublle ${d.data.group}`.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, ''));

  leaf.append("circle")
      .attr("id", d => (d.leafUid = uid("leaf")).id)
      .attr("r", d => d.r)
      .attr("fill-opacity", 0.7)
      .attr("fill", d => color(color_index[d.data.group]))
      .attr("stroke", "grey")
      .attr("stroke-width", "2px")
      .attr("stroke-linecap", "round")
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide);
    
  //leaf.append()

  leaf.append("clipPath")
      .attr("id", d => (d.clipUid = uid("clip")).id)
    .append("use")
      .attr("xlink:href", d => d.leafUid.href);

  leaf.append("text")
      .attr("clip-path", d => d.clipUid)
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide)
    .selectAll("tspan")
    .data(d => d.data.name.split(/(?=[A-Z][a-z])|\s+/g))
    .join("tspan")
      .attr("class", "text-break")
      .attr("x", 0)
      .attr("y", (d, i, nodes) => `${i - nodes.length / 2 + 0.8}em`)
      .text(d => d);

  /*leaf.append("title")
      .text(d => `${d.data.title === undefined ? "" : `${d.data.title}
`}${format(d.value)}`);*/
    
  return svg.node();
}

pack = data => d3.pack()
    .size([width - 2, height - 2])
    .padding(3)
  (d3.hierarchy({children: data})
    .sum(d => d.value))

width = 932
height = width

format = d3.format(",d")
