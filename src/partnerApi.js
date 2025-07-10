// partnerApi.js
const express = require('express');
const bodyParser = require('body-parser');

class PartnerAPI {
    constructor(port, broadcastSync) {
        this.port = port;
        this.broadcastSync = broadcastSync;
        this.app = express();
        this.app.use(bodyParser.json());

        this.app.post('/api/sync', (req, res) => {
            const { value, totalSupply } = req.body;
            if (value && totalSupply) {
                this.broadcastSync.updateValue(value, totalSupply);
                res.status(200).send({ message: 'Synchronized successfully' });
            } else {
                res.status(400).send({ error: 'Invalid data' });
            }
        });

        this.app.listen(this.port, () => {
            console.log(`Partner API listening on port ${this.port}`);
        });
    }
}

module.exports = PartnerAPI;
