const ARES = require('./ares/ares_core');
const Logger = require('./logger'); // Assuming you have a logger utility
const process = require('process');

async function startSupernode() {
  const ares = new ARES();

  try {
    await ares.initialize();
    Logger.info('Pi-Supernode running with ARES');
  } catch (error) {
    Logger.error('Failed to initialize ARES:', error);
    process.exit(1); // Exit with a failure code
  }

  // Handle graceful shutdown
  process.on('SIGINT', async () => {
    Logger.info('Shutting down Pi-Supernode...');
    // Perform any necessary cleanup here
    await ares.cleanup(); // Assuming you implement a cleanup method in ARES
    Logger.info('Pi-Supernode has been shut down gracefully.');
    process.exit(0); // Exit with a success code
  });

  process.on('SIGTERM', async () => {
    Logger.info('Received SIGTERM. Shutting down Pi-Supernode...');
    await ares.cleanup(); // Assuming you implement a cleanup method in ARES
    Logger.info('Pi-Supernode has been shut down gracefully.');
    process.exit(0); // Exit with a success code
  });
}

startSupernode();
