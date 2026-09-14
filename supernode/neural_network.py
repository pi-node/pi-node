import numpy as np
import tensorflow as tf

class NeuralNetwork:
    def __init__(self, input_dim, hidden_dim, output_dim):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(hidden_dim, activation='relu', input_shape=(input_dim,)),
            tf.keras.layers.Dense(output_dim)
        ])
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def train(self, X, y):
        self.model.fit(X, y, epochs=100, batch_size=32)

    def predict(self, X):
        return self.model.predict(X)

# Example usage:
nn = NeuralNetwork(10, 20, 1)
X = np.random.rand(100, 10)
y = np.random.rand(100, 1)
nn.train(X, y)
predictions = nn.predict(X)
