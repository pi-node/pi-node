const d3 = require('d3-array');
const WebSocket = require('ws');

const ws = new WebSocket('wss://pi-supernode.com/ws');

ws.on('message', (message) => {
  const data = JSON.parse(message);
  const nodes = data.nodes;
  const edges = data.edges;

  // Update network visualization
  d3.select('#network')
    .selectAll('circle')
    .data(nodes)
    .enter()
    .append('circle')
    .attr('cx', (d) => d.x)
    .attr('cy', (d) => d.y)
    .attr('r', 5);

  d3.select('#network')
    .selectAll('line')
    .data(edges)
    .enter()
    .append('line')
    .attr('x1', (d) => d.source.x)
    .attr('y1', (d) => d.source.y)
    .attr('x2', (d) => d.target.x)
    .attr('y2', (d) => d.target.y);
});
