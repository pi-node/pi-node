const tf = require('@tensorflow/tfjs');

/**
 * Creates a simple neural network model for transaction prediction
 * @returns {tf.LayersModel} - The compiled model
 */
function createModel() {
    const model = tf.sequential();
    model.add(tf.layers.dense({ units: 64, activation: 'relu', inputShape: [5] })); // Input layer
    model.add(tf.layers.dense({ units: 32, activation: 'relu' })); // Hidden layer
    model.add(tf.layers.dense({ units: 1 })); // Output layer for regression

    model.compile({
        optimizer: 'adam',
        loss: 'meanSquaredError',
        metrics: ['mae']
    });

    return model;
}

/**
 * Trains the transaction prediction model
 * @param {tf.Tensor} xTrain - Training data (features)
 * @param {tf.Tensor} yTrain - Training labels (transaction amounts)
 * @param {number} epochs - Number of training epochs
 * @param {number} batchSize - Size of each training batch
 * @returns {Promise} - Promise that resolves when training is complete
 */
async function trainModel(model, xTrain, yTrain, epochs = 100, batchSize = 32) {
    return await model.fit(xTrain, yTrain, {
        epochs: epochs,
        batchSize: batchSize,
        validationSplit: 0.2,
        callbacks: {
            onEpochEnd: (epoch, logs) => {
                console.log(`Epoch ${epoch + 1}: loss = ${logs.loss}, mae = ${logs.mae}`);
            }
        }
    });
}

/**
 * Predicts transaction amounts based on input data
 * @param {tf.Tensor} inputData - Data to predict
 * @returns {tf.Tensor} - Predictions
 */
function predictTransactions(model, inputData) {
    return model.predict(inputData);
}

/**
 * Example usage of the transaction prediction model
 */
async function main() {
    // Create the model
    const model = createModel();

    // Generate some synthetic training data
    const xTrain = tf.randomNormal([1000, 5]); // 1000 samples, 5 features (e.g., previous transaction amounts, time, etc.)
    const yTrain = tf.randomNormal([1000, 1]).add(100); // Transaction amounts centered around 100

    // Train the model
    await trainModel(model, xTrain, yTrain);

    // Generate some test data
    const testData = tf.randomNormal([10, 5]); // 10 samples, 5 features
    const predictions = predictTransactions(model, testData);

    // Print predictions
    predictions.print();
}

// Run the example
main();

module.exports = {
    createModel,
    trainModel,
    predictTransactions
};
