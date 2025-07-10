# data_visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

class DataVisualization:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def visualize_distribution(self, feature: str) -> None:
        plt.hist(self.data[feature], bins=50)
        plt.title(f'Distribution of {feature}')
        plt.show()

    def visualize_correlation(self) -> None:
        sns.heatmap(self.data.corr(), annot=True, cmap='coolwarm', square=True)
        plt.show()

    def visualize_3d_scatter(self, x: str, y: str, z: str) -> None:
        fig = go.Figure(data=[go.Scatter3d(
            x=self.data[x],
            y=self.data[y],
            z=self.data[z],
            mode='markers',
            marker=dict(
                size=5,
                color=self.data['target'],
                colorscale='Viridis',
                showscale=True
            )
        )])
        fig.update_layout(title=f'3D Scatter Plot of {x}, {y}, and {z}')
        fig.show()
