import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from lime import lime_tabular

class ExplainableAIService:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.explainer = lime_tabular.LimeTabularExplainer

    def train(self, X, y):
        # Train the model
        self.model.fit(X, y)

    def explain(self, X, y):
        # Explain the model using LIME
        explainer = self.explainer(X, self.model.predict_proba, num_features=5)
        explanation = explainer.explain_instance(X, y)
        return explanation
