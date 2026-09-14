import numpy as np
from sklearn.cluster import KMeans

class AdvancedClustering:
    def __init__(self, node_data, num_clusters):
        self.node_data = node_data
        self.num_clusters = num_clusters
        self.kmeans = KMeans(n_clusters=num_clusters)

    def cluster_nodes(self):
        self.kmeans.fit(self.node_data)
        labels = self.kmeans.labels_
        return labels

    def get_centroids(self):
        return self.kmeans.cluster_centers_

# Example usage:
node_data = np.random.rand(100, 10)
clustering = AdvancedClustering(node_data, 5)
labels = clustering.cluster_nodes()
centroids = clustering.get_centroids()
