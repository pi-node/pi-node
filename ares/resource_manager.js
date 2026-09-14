const os = require('os');
const { exec } = require('child_process');
const winston = require('winston');
const nodemailer = require('nodemailer'); // For email notifications
const fs = require('fs');
const path = require('path');

class ResourceManager {
  constructor(config) {
    this.config = config;
    this.history = [];
    this.setupLogger();
    this.setupEmailNotifications();
  }

  setupLogger() {
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
      ),
      transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'resource_manager.log' })
      ]
    });
  }

  setupEmailNotifications() {
    this.transporter = nodemailer.createTransport({
      service: 'gmail', // Use your email service
      auth: {
        user: this.config.email.user,
        pass: this.config.email.pass
      }
    });
  }

  async sendEmailNotification(subject, message) {
    const mailOptions = {
      from: this.config.email.user,
      to: this.config.email.recipient,
      subject: subject,
      text: message
    };

    try {
      await this.transporter.sendMail(mailOptions);
      this.logger.info('Email notification sent successfully.');
    } catch (error) {
      this.logger.error('Error sending email notification:', error);
    }
  }

  getCPUUsage() {
    const cpus = os.cpus();
    const total = cpus.length;
    const idle = cpus.reduce((acc, cpu) => acc + cpu.times.idle, 0);
    const totalTimes = cpus.reduce((acc, cpu) => acc + Object.values(cpu.times).reduce((a, b) => a + b, 0), 0);
    return ((totalTimes - idle) / totalTimes) * 100; // Return CPU usage percentage
  }

  getMemoryUsage() {
    const totalMemory = os.totalmem();
    const freeMemory = os.freemem();
    return ((totalMemory - freeMemory) / totalMemory) * 100; // Return memory usage percentage
  }

  getDiskUsage() {
    return new Promise((resolve, reject) => {
      exec('df -h', (error, stdout, stderr) => {
        if (error) {
          this.logger.error(`Error getting disk usage: ${stderr}`);
          return reject(error);
        }
        const diskUsage = stdout.split('\n').slice(1).map(line => {
          const parts = line.split(/\s+/);
          return {
            filesystem: parts[0],
            size: parts[1],
            used: parts[2],
            available: parts[3],
            usePercentage: parts[4],
            mountedOn: parts[5]
          };
        }).filter(disk => disk.filesystem);
        resolve(diskUsage);
      });
    });
  }

  checkResourceThresholds(cpuThreshold, memoryThreshold) {
    const cpuUsage = this.getCPUUsage();
    const memoryUsage = this.getMemoryUsage();

    if (cpuUsage > cpuThreshold) {
      const message = `High CPU usage detected: ${cpuUsage.toFixed(2)}% (Threshold: ${cpuThreshold}%)`;
      this.logger.warn(message);
      this.sendEmailNotification('High CPU Usage Alert', message);
    }
    if (memoryUsage > memoryThreshold) {
      const message = `High memory usage detected: ${memoryUsage.toFixed(2)}% (Threshold: ${memoryThreshold}%)`;
      this.logger.warn(message);
      this.sendEmailNotification('High Memory Usage Alert', message);
    }
  }

  logResourceUsage() {
    const usage = {
      timestamp: new Date(),
      cpu: this.getCPUUsage(),
      memory: this.getMemoryUsage()
    };
    this.history.push(usage);
    fs.append FileSync(path.join(__dirname, 'resource_usage_history.json'), JSON.stringify(usage) + '\n');
    this.logger.info('Resource usage logged:', usage);
  }

  async monitorResources(interval = 5000) {
    setInterval(async () => {
      this.checkResourceThresholds(this.config.thresholds.cpu, this.config.thresholds.memory);
      this.logResourceUsage();
      const diskUsage = await this.getDiskUsage();
      this.logger.info('Current Disk Usage:', diskUsage);
    }, interval);
  }

  healthCheck() {
    const cpuUsage = this.getCPUUsage();
    const memoryUsage = this.getMemoryUsage();
    const healthStatus = {
      cpuUsage,
      memoryUsage,
      diskUsage: this.getDiskUsage(),
      timestamp: new Date()
    };
    this.logger.info('Health Check Status:', healthStatus);
    return healthStatus;
  }

  // Additional methods for dynamic resource management can be added here
}

module.exports = ResourceManager;
