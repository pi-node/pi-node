const gremlin = require('gremlin');

const graph = new gremlin.Graph();
const query = 'g.V().has("name", "marko").out("knows")';
const results = graph.execute(query);

console.log(results);
