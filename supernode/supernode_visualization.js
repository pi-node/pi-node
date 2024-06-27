const WebSocket = require('ws');
const Chart = require('chart.js');

class SupernodeVisualization {
  constructor() {
    this.ws = new WebSocket.Server({ port: 8080 });
    this.chart = new Chart('chart', {
      type: 'line',
      data: {
        labels: [],
        datasets: [{
          label: 'Temperature',
          data: [],
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }

  async sendData(data) {
    this.ws.clients.forEach(client => {
      client.send(JSON.stringify(data));
    });
  }

  async updateChart(data) {
    this.chart.data.labels.push(new Date().toLocaleTimeString());
    this.chart.data.datasets[0].data.push(data.temperature);
    this.chart.update();
  }
}

module.exports = SupernodeVisualization;
