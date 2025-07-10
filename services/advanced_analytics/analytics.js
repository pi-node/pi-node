const tf = require('@tensorflow/tfjs');

const nodeData = [
  { cpuUsage: 0.5, memoryUsage: 0.3, networkUsage: 0.2 },
  { cpuUsage: 0.2, memoryUsage: 0.1, networkUsage: 0.4 },
  // ...
];

const model = tf.sequential();
model.add(tf.layers.dense({ units: 3, inputShape: [3] }));
model.add(tf.layers.dense({ units: 1 }));
model.compile({ optimizer: tf.optimizers.adam(), loss: 'meanSquaredError' });

const predictNodeBehavior = async (nodeId) => {
  const inputData = nodeData.find((data) => data.nodeId === nodeId);
  const output = model.predict(inputData);
  console.log(`Predicted node behavior: ${output}`);
};
