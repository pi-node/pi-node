const AWS = require('aws-sdk');

class SupernodeCloud {
  constructor() {
    this.s3 = new AWS.S3({ region: 'your_region' });
  }

  async sendToCloud(data) {
    const params = {
      Bucket: 'your_bucket_name',
      Key: 'ensor_data.json',
      Body: JSON.stringify(data)
    };
    this.s3.putObject(params, (err, data) => {
      if (err) console.log(err);
      else console.log(`Data sent to cloud: ${data}`);
    });
  }
}

module.exports = SupernodeCloud;
