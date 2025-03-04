const tf = require('@tensorflow/tfjs');

/**
 * Creates a simple neural network model for anomaly detection
 * @returns {tf.LayersModel} - The compiled model
 */
function createModel() {
    const model = tf.sequential();
    model.add(tf.layers.dense({ units: 32, activation: 'relu', inputShape: [10] })); // Input layer
    model.add(tf.layers.dense({ units: 16, activation: 'relu' })); // Hidden layer
    model.add(tf.layers.dense({ units: 1, activation: 'sigmoid' })); // Output layer for binary classification

    model.compile({
        optimizer: 'adam',
        loss: 'binaryCrossentropy',
        metrics: ['accuracy']
    });

    return model;
}

/**
 * Trains the anomaly detection model
 * @param {tf.Tensor} xTrain - Training data
 * @param {tf.Tensor} yTrain - Training labels
 * @param {number} epochs - Number of training epochs
 * @param {number} batchSize - Size of each training batch
 * @returns {Promise} - Promise that resolves when training is complete
 */
async function trainModel(model, xTrain, yTrain, epochs = 50, batchSize = 32) {
    return await model.fit(xTrain, yTrain, {
        epochs: epochs,
        batchSize: batchSize,
        validationSplit: 0.2,
        callbacks: {
            onEpochEnd: (epoch, logs) => {
                console.log(`Epoch ${epoch + 1}: loss = ${logs.loss}, accuracy = ${logs.acc}`);
            }
        }
    });
}

/**
 * Predicts anomalies in the input data
 * @param {tf.Tensor} inputData - Data to predict
 * @returns {tf.Tensor} - Predictions
 */
function predictAnomalies(model, inputData) {
    return model.predict(inputData);
}

/**
 * Example usage of the anomaly detection model
 */
async function main() {
    // Create the model
    const model = createModel();

    // Generate some synthetic training data
    const xTrain = tf.randomNormal([1000, 10]); // 1000 samples, 10 features
    const yTrain = tf.randomUniform([1000, 1]).greater(0.8).toFloat(); // 20% anomalies

    // Train the model
    await trainModel(model, xTrain, yTrain);

    // Generate some test data
    const testData = tf.randomNormal([10, 10]); // 10 samples, 10 features
    const predictions = predictAnomalies(model, testData);

    // Print predictions
    predictions.print();
}

// Run the example
main();

module.exports = {
    createModel,
    trainModel,
    predictAnomalies
};
