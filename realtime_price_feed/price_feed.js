const WebSocket = require('ws');
const ccxt = require('ccxt');

const ws = new WebSocket('wss://stream.binance.com:9443/stream');

ws.on('message', (message) => {
  const data = JSON.parse(message);
  const price = data.data.k.c;
  console.log(`Real-time price: ${price}`);
});

const exchange = new ccxt.binance({
  apiKey: 'YOUR_API_KEY',
  apiSecret: 'YOUR_API_SECRET',
});

exchange.fetchTickers().then((tickers) => {
  console.log(tickers);
});
