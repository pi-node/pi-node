const { Node } = require('./node');
const { WebSocket } = require('ws');

class Analytics {
  constructor() {
    this.ws = new WebSocket.Server({ port: 8080 });
    this.nodes = {};
  }

  async start() {
    this.ws.on('connection', (ws) => {
      ws.on('message', (message) => {
        const { type, data } = JSON.parse(message);
        if (type === 'NODE_METRICS') {
          this.nodes[data.nodeId] = data.metrics;
          this.broadcastMetrics();
        }
      });
    });
  }

  async broadcastMetrics() {
    const metrics = Object.values(this.nodes).reduce((acc, metrics) => {
      acc.cpuUsage += metrics.cpuUsage;
      acc.memoryUsage += metrics.memoryUsage;
      return acc;
    }, { cpuUsage: 0, memoryUsage: 0 });
    this.ws.clients.forEach((client) => client.send(JSON.stringify({ type: 'METRICS', data: metrics })));
  }
}

module.exports = Analytics;
