const { Node } = require('./node');
const { Cluster } = require('cluster');

class SupernodeManager {
  constructor() {
    this.nodes = [];
    this.cluster = new Cluster();
  }

  async start() {
    await this.cluster.setup({
      exec: 'node',
      args: ['--experimental-modules', 'node.js'],
    });

    for (let i = 0; i < 5; i++) {
      const worker = this.cluster.fork();
      worker.send({ type: 'START_NODE' });
      this.nodes.push(worker);
    }
  }

  async stop() {
    await Promise.all(this.nodes.map((worker) => worker.send({ type: 'STOP_NODE' })));
    this.cluster.disconnect();
  }

  async broadcast(message) {
    this.nodes.forEach((worker) => worker.send(message));
  }
}

module.exports = SupernodeManager;
