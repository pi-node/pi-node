# predictive_model.py
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

class PredictiveModel:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.model: GradientBoostingRegressor = None

    def train_model(self, data: pd.DataFrame) -> None:
        self.model = GradientBoostingRegressor()
        self.model.fit(data.drop('target', axis=1), data['target'])

    def predict(self, features: pd.DataFrame) -> np.ndarray:
        return self.model.predict(features)
