const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const nodemailer = require('nodemailer');
const winston = require('winston');
const axios = require('axios'); // For external threat intelligence
const { performance } = require('perf_hooks'); // For performance monitoring

class ThreatDetector {
  constructor(config) {
    this.config = config;
    this.setupLogger();
    this.setupEmailNotifications();
    this.suspiciousActivityLog = [];
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
        new winston.transports.File({ filename: 'threat_detector.log' })
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

  monitorLogs() {
    const logFilePath = '/var/log/auth.log'; // Path to the log file to monitor
    fs.watchFile(logFilePath, (curr, prev) => {
      fs.readFile(logFilePath, 'utf8', (err, data) => {
        if (err) {
          this.logger.error('Error reading log file:', err);
          return;
        }
        this.checkForSuspiciousActivity(data);
      });
    });
  }

  checkForSuspiciousActivity(logData) {
    const suspiciousPatterns = [
      /Failed password for invalid user/, // Example pattern for failed login attempts
      /Failed password for root/, // Example pattern for root login attempts
      /authentication failure/, // General authentication failure
      /Unauthorized access/, // Example pattern for unauthorized access
      /malicious activity detected/ // Example pattern for malicious activity
    ];

    suspiciousPatterns.forEach(pattern => {
      if (pattern.test(logData)) {
        const message = 'Suspicious activity detected in logs.';
        this.logger.warn(message);
        this.suspiciousActivityLog.push({ timestamp: new Date(), message });
        this.sendEmailNotification('Suspicious Activity Alert', message);
      }
    });
  }

  async checkForVulnerabilities() {
    return new Promise((resolve, reject) => {
      exec('npm audit --json', (error, stdout, stderr) => {
        if (error) {
          this.logger.error(`Error checking for vulnerabilities: ${stderr}`);
          return reject(error);
        }
        const auditReport = JSON.parse(stdout);
        if (auditReport.metadata.vulnerabilities.total > 0) {
          const message = `Vulnerabilities detected: ${JSON.stringify(auditReport)}`;
          this.logger.warn(message);
          this.sendEmailNotification('Vulnerability Alert', message);
        }
        resolve(auditReport);
      });
    });
  }

  async fetchThreatIntelligence() {
    try {
      const response = await axios.get(this.config.threatIntelligence.apiUrl);
      if (response.data && response.data.threats) {
        this.logger.info('Threat intelligence data fetched successfully.');
        return response.data.threats;
      }
    } catch (error) {
      this.logger.error('Error fetching threat intelligence:', error);
    }
  }

  async analyzeAnomalies() {
    const cpuUsage = await this.getCPUUsage();
    const memoryUsage = await this.getMemoryUsage();
    const threshold = this.config.anomalyDetection.threshold;

    if (cpuUsage > threshold.cpu || memoryUsage > threshold.memory) {
      const message = `Anomaly detected: CPU Usage: ${cpuUsage.toFixed(2)}%, Memory Usage: ${memoryUsage.toFixed(2)}%`;
      this.logger.warn(message);
      this.sendEmailNotification('Anomaly Detection Alert', message);
    }
  }

  async getCPUUsage() {
    // Implement CPU usage retrieval logic
    return new Promise((resolve) => {
      exec("top -bn 1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{print 100 - $1}'", (error, stdout) => {
        if (error) {
          this.logger.error('Error retrieving CPU usage:', error);
          resolve(0);
        } else {
          resolve(parseFloat(stdout));
        }
      });
    });
  }

  async getMemoryUsage() {
    // Implement memory usage retrieval logic
    return new Promise((resolve) => {
      exec("free | grep Mem | awk '{print $3/$2 * 100.0}'", (error, stdout) => {
        if (error) {
          this.logger.error('Error retrieving memory usage:', error);
          resolve(0);
        } else {
          resolve(parseFloat(stdout));
        }
      });
    });
  }

  async runThreatDetection() {
    this.monitorLogs();
    await this.checkForVulnerabilities();
    await this.fetchThreatIntelligence();
    await this.analyzeAnomalies();
    // Additional threat detection methods can be called here
  }
}

module.exports = ThreatDetector;
