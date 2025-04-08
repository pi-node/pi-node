import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

class EdgeAIService:
    def __init__(self):
        self.model = Model(inputs=Input(shape=(10,)), outputs=Dense(10, activation='softmax'))

    def train(self, X, y):
        # Train the lightweight neural network
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(X, y, epochs=10)

    def predict(self, X):
        # Make predictions using the lightweight neural network
        return self.model.predict(X)
