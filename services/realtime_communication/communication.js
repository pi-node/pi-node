const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  console.log('Node connected');

  ws.on('message', (message) => {
    console.log(`Received message from node: ${message}`);
    // Broadcast message to other nodes
    wss.clients.forEach((client) => {
      client.send(message);
    });
  });

  ws.on('close', () => {
    console.log('Node disconnected');
  });
});
