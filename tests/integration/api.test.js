// tests/integration/api.test.js

const request = require('supertest');
const express = require('express');
const app = require('../../src/index'); // Import your Express app

describe('API Integration Tests', () => {
    it('should get the balance of a specific account', async () => {
        const response = await request(app)
            .get('/api/stablecoin/balance/GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            .set('Authorization', 'Bearer your_jwt_token_here'); // Replace with a valid token

        expect(response.status).toBe(200);
        expect(response.body).toHaveProperty('balance');
    });

    it('should send Pi Coin from one account to another', async () => {
        const response = await request(app)
            .post('/api/stablecoin/send')
            .set('Authorization', 'Bearer your_jwt_token_here') // Replace with a valid token
            .send({
                from: 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
                to: 'GYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',
                amount: '10',
                secret: 'SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', // Replace with a valid secret
            });

        expect(response.status).toBe(200);
        expect(response.body).toHaveProperty('transactionHash');
    });

    it('should create a new governance proposal', async () => {
        const response = await request(app)
            .post('/api/governance/propose')
            .set('Authorization', 'Bearer your_jwt_token_here') // Replace with a valid token
            .send({
                title: 'New Proposal',
                description: 'Description of the new proposal',
                proposer: 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            });

        expect(response.status).toBe(200);
        expect(response.body).toHaveProperty('message', 'Proposal created successfully');
    });

    it('should record a vote on a governance proposal', async () => {
        const response = await request(app)
            .post('/api/governance/vote')
            .set('Authorization', 'Bearer your_jwt_token_here') // Replace with a valid token
            .send({
                proposalId: 'mockProposalId',
                voter: 'GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
                vote: 'yes',
            });

        expect(response.status).toBe(200);
        expect(response.body).toHaveProperty('message', 'Vote recorded successfully');
    });
});
