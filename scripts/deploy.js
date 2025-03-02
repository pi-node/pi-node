// scripts/deploy.js

const { exec } = require('child_process');
const dotenv = require('dotenv');

// Load environment variables from .env file
dotenv.config();

const deploySmartContracts = async () => {
    return new Promise((resolve, reject) => {
        exec('npx hardhat run scripts/deployContracts.js --network yourNetwork', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error deploying contracts: ${error.message}`);
                return reject(error);
            }
            if (stderr) {
                console.error(`Deployment stderr: ${stderr}`);
                return reject(new Error(stderr));
            }
            console.log(`Deployment stdout: ${stdout}`);
            resolve(stdout);
        });
    });
};

const main = async () => {
    try {
        console.log('Starting deployment...');
        await deploySmartContracts();
        console.log('Deployment completed successfully.');
    } catch (error) {
        console.error('Deployment failed:', error);
    }
};

main();
