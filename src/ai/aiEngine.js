const { createModel: createAnomalyModel, trainModel: trainAnomalyModel, predictAnomalies } = require('./models/anomalyDetectionModel');
const { createModel: createTransactionModel, trainModel: trainTransactionModel, predictTransactions } = require('./models/transactionPredictionModel');
const tf = require('@tensorflow/tfjs');

/**
 * Main AI Engine class for processing data
 */
class AIEngine {
    constructor() {
        this.anomalyModel = createAnomalyModel();
        this.transactionModel = createTransactionModel();
    }

    /**
     * Trains both the anomaly detection and transaction prediction models
     * @param {tf.Tensor} xAnomalyTrain - Training data for anomaly detection
     * @param {tf.Tensor} yAnomalyTrain - Training labels for anomaly detection
     * @param {tf.Tensor} xTransactionTrain - Training data for transaction prediction
     * @param {tf.Tensor} yTransactionTrain - Training labels for transaction prediction
     * @returns {Promise} - Promise that resolves when both models are trained
     */
    async trainModels(xAnomalyTrain, yAnomalyTrain, xTransactionTrain, yTransactionTrain) {
        console.log("Training Anomaly Detection Model...");
        await trainAnomalyModel(this.anomalyModel, xAnomalyTrain, yAnomalyTrain);
        
        console.log("Training Transaction Prediction Model...");
        await trainTransactionModel(this.transactionModel, xTransactionTrain, yTransactionTrain);
    }

    /**
     * Predicts anomalies in the input data
     * @param {tf.Tensor} inputData - Data to predict anomalies
     * @returns {tf.Tensor} - Anomaly predictions
     */
    predictAnomalies(inputData) {
        return predictAnomalies(this.anomalyModel, inputData);
    }

    /**
     * Predicts transaction amounts based on input data
     * @param {tf.Tensor} inputData - Data to predict transaction amounts
     * @returns {tf.Tensor} - Transaction predictions
     */
    predictTransactions(inputData) {
        return predictTransactions(this.transactionModel, inputData);
    }
}

/**
 * Example usage of the AI Engine
 */
async function main() {
    const aiEngine = new AIEngine();

    // Generate synthetic training data for anomaly detection
    const xAnomalyTrain = tf.randomNormal([1000, 10]); // 1000 samples, 10 features
    const yAnomalyTrain = tf.randomUniform([1000, 1]).greater(0.8).toFloat(); // 20% anomalies

    // Generate synthetic training data for transaction prediction
    const xTransactionTrain = tf.randomNormal([1000, 5]); // 1000 samples, 5 features
    const yTransactionTrain = tf.randomNormal([1000, 1]).add(100); // Transaction amounts centered around 100

    // Train both models
    await aiEngine.trainModels(xAnomalyTrain, yAnomalyTrain, xTransactionTrain, yTransactionTrain);

    // Generate some test data for predictions
    const testAnomalyData = tf.randomNormal([10, 10]); // 10 samples, 10 features
    const anomalyPredictions = aiEngine.predictAnomalies(testAnomalyData);
    console.log("Anomaly Predictions:");
    anomalyPredictions.print();

    const testTransactionData = tf.randomNormal([10, 5]); // 10 samples, 5 features
    const transactionPredictions = aiEngine.predictTransactions(testTransactionData);
    console.log("Transaction Predictions:");
    transactionPredictions.print();
}

// Run the example
main();

module.exports = AIEngine;
