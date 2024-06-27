# data_visualizer.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class DataVisualizer:
    def __init__(self, nodes: List[dict]):
        self.nodes = nodes
        self.fig, self.ax = plt.subplots()

    def update_plot(self, i):
        node_data = [(node['cpu_usage'], node['memory_usage']) for node in self.nodes]
        self.ax.clear()
        self.ax.scatter(*zip(*node_data))
        self.ax.set_xlabel('CPU Usage')
        self.ax.set_ylabel('Memory Usage')

    def start_visualization(self):
        ani = animation.FuncAnimation(self.fig, self.update_plot, interval=1000)
        plt.show()

data_visualizer = DataVisualizer(optimized_nodes)
data_visualizer.start_visualization()
