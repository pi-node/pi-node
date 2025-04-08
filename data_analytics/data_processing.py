# data_processing.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

class DataProcessing:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def preprocess_data(self) -> pd.DataFrame:
        scaler = StandardScaler()
        self.data[['feature1', 'feature2', 'feature3']] = scaler.fit_transform(self.data[['feature1', 'feature2', 'feature3']])
        return self.data

    def feature_engineering(self) -> pd.DataFrame:
        pca = PCA(n_components=2)
        self.data[['feature1_pca', 'feature2_pca']] = pca.fit_transform(self.data[['feature1', 'feature2']])
        return self.data

    def train_model(self) -> RandomForestClassifier:
        X = self.data.drop('target', axis=1)
        y = self.data['target']
        model = RandomForestClassifier()
        model.fit(X, y)
        return model
