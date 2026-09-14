const { performance } = require('perf_hooks');
const WebSocket = require('ws');

class MonitoringAgent {
  constructor(nodeId, wsUrl) {
    this.nodeId = nodeId;
    this.wsUrl = wsUrl;
    this.ws = new WebSocket(wsUrl);
    this.metrics = {};
  }

  async startMonitoring() {
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.metrics[data.metric] = data.value;
    };
    this.ws.onopen = () => {
      console.log(`Connected to node ${this.nodeId}`);
      this.sendMetric('cpu_usage', 0);
      this.sendMetric('memory_usage', 0);
    };
  }

  async sendMetric(metric, value) {
    this.ws.send(JSON.stringify({ metric, value }));
  }

  async getMetrics() {
    return this.metrics;
  }
}

module.exports = MonitoringAgent;
