const tf = require('@tensorflow/tfjs');

/**
 * Normalizes a tensor to a range of [0, 1]
 * @param {tf.Tensor} tensor - The tensor to normalize
 * @returns {tf.Tensor} - The normalized tensor
 */
function normalizeTensor(tensor) {
    const min = tensor.min();
    const max = tensor.max();
    return tensor.sub(min).div(max.sub(min));
}

/**
 * Splits a dataset into training and testing sets
 * @param {tf.Tensor} data - The dataset to split
 * @param {number} trainFraction - The fraction of data to use for training
 * @returns {Object} - An object containing training and testing tensors
 */
function splitDataset(data, trainFraction = 0.8) {
    const numSamples = data.shape[0];
    const numTrainSamples = Math.floor(numSamples * trainFraction);
    
    const trainData = data.slice([0, 0], [numTrainSamples, -1]);
    const testData = data.slice([numTrainSamples, 0], [numSamples - numTrainSamples, -1]);
    
    return { trainData, testData };
}

/**
 * Calculates Mean Absolute Error (MAE)
 * @param {tf.Tensor} yTrue - True labels
 * @param {tf.Tensor} yPred - Predicted labels
 * @returns {number} - The calculated MAE
 */
function calculateMAE(yTrue, yPred) {
    return yTrue.sub(yPred).abs().mean().arraySync();
}

/**
 * Calculates Mean Squared Error (MSE)
 * @param {tf.Tensor} yTrue - True labels
 * @param {tf.Tensor} yPred - Predicted labels
 * @returns {number} - The calculated MSE
 */
function calculateMSE(yTrue, yPred) {
    return yTrue.sub(yPred).square().mean().arraySync();
}

/**
 * Example usage of utility functions
 */
function main() {
    // Create a sample tensor
    const data = tf.tensor2d([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]);
    
    // Normalize the tensor
    const normalizedData = normalizeTensor(data);
    console.log("Normalized Data:");
    normalizedData.print();
    
    // Split the dataset
    const { trainData, testData } = splitDataset(data);
    console.log("Training Data:");
    trainData.print();
    console.log("Testing Data:");
    testData.print();
    
    // Calculate MAE and MSE
    const yTrue = tf.tensor2d([[1], [2], [3]]);
    const yPred = tf.tensor2d([[1.1], [1.9], [3.2]]);
    
    const mae = calculateMAE(yTrue, yPred);
    const mse = calculateMSE(yTrue, yPred);
    
    console.log("Mean Absolute Error (MAE):", mae);
    console.log("Mean Squared Error (MSE):", mse);
}

// Run the example
main();

module.exports = {
    normalizeTensor,
    splitDataset,
    calculateMAE,
    calculateMSE
};
