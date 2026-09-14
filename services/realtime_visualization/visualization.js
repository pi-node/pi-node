const d3 = require('d3');

const nodeData = [
  { cpuUsage: 0.5, memoryUsage: 0.3, networkUsage: 0.2 },
  { cpuUsage: 0.2, memoryUsage: 0.1, networkUsage: 0.4 },
  //...
];

const svg = d3.select('body')
 .append('svg')
 .attr('width', 500)
 .attr('height', 500);

const nodes = svg.selectAll('circle')
 .data(nodeData)
 .enter()
 .append('circle')
 .attr('cx', (d) => d.cpuUsage * 100)
 .attr('cy', (d) => d.memoryUsage * 100)
 .attr('r', 5);
