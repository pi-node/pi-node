const { Brain } = require('brain.js');
const { Node } = require('./node');

class AIOptimizer {
  constructor() {
    this.brain = new Brain.NeuralNetwork();
    this.trainingData = [];
  }

  async train() {
    const trainingData = await this.collectTrainingData();
    this.brain.train(trainingData);
  }

  async collectTrainingData() {
    const nodeMetrics = await Promise.all(
      Array(10).fill(0).map(() => Node.getMetrics())
    );
    return nodeMetrics.map((metrics) => ({
      input: [metrics.cpuUsage, metrics.memoryUsage],
      output: [metrics.optimizationScore],
    }));
  }

  async optimizeNode(node) {
    const input = [node.cpuUsage, node.memoryUsage];
    const output = this.brain.run(input);
    return output[0];
  }
}

module.exports = AIOptimizer;
