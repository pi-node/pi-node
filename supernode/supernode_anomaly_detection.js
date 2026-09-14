const brain = require('brain.js');

class SupernodeAnomalyDetection {
  constructor() {
    this.net = new brain.NeuralNetwork();
    this.net.fromJSON({
      "layers": [
        {"input": "x"},
        {"hidden": 10},
        {"output": "y"}
      ]
    });
  }

  async train(data) {
    this.net.train(data);
  }

  async detectAnomaly(data) {
    const output = this.net.run(data);
    return output > 0.5? true : false; // adjust the threshold as needed
  }
}

module.exports = SupernodeAnomalyDetection;
