const sklearn = require('sklearn');

const nodeData = [
  { cpuUsage: 0.5, memoryUsage: 0.3, networkUsage: 0.2 },
  { cpuUsage: 0.2, memoryUsage: 0.1, networkUsage: 0.4 },
  //...
];

const kmeans = new sklearn.KMeans({ nClusters: 3 });
const clusters = kmeans.fit(nodeData);
console.log(`Node clusters: ${clusters}`);
