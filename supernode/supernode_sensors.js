const sensorLib = require('node-dht-sensor');
const gps = require('gps');

class SupernodeSensors {
  constructor() {
    this.dht11 = new sensorLib.Sensor(11, 4); // DHT11 temperature and humidity sensor
    this.gpsModule = new gps.GPS();
  }

  async readSensors() {
    const temperature = await this.dht11.readTemperature();
    const humidity = await this.dht11.readHumidity();
    const gpsData = await this.gpsModule.getData();
    return { temperature, humidity, gpsData };
  }
}

module.exports = SupernodeSensors;
