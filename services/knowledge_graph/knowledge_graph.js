const gremlin = require('gremlin');

const graph = new gremlin.Graph();
graph.addVertex('node1', { label: 'Node' });
graph.addVertex('node2', { label: 'Node' });
graph.addEdge('node1', 'node2', { label: 'Connected' });

const query = graph.traversal().V().hasLabel('Node').out('Connected');
const results = query.execute();
console.log(results);
