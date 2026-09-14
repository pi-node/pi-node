// broadcastSync.js
const WebSocket = require('ws');

class BroadcastSync {
    constructor(port) {
        this.port = port;
        this.wss = new WebSocket.Server({ port: this.port });
        this.clients = new Set();
        
        this.wss.on('connection', (ws) => {
            this.clients.add(ws);
            console.log('New client connected');

            ws.on('close', () => {
                this.clients.delete(ws);
                console.log('Client disconnected');
            });
        });
    }

    broadcast(message) {
        for (const client of this.clients) {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify(message));
            }
        }
        console.log('Broadcasted message:', message);
    }

    updateValue(newValue, totalSupply) {
        const message = {
            type: 'UPDATE',
            value: newValue,
            totalSupply: totalSupply,
            timestamp: Date.now(),
        };
        this.broadcast(message);
    }
}

module.exports = BroadcastSync;
