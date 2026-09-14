const { Node } = require('./node');
const { Level } = require('level');

class Database {
  constructor() {
    this.db = new Level('supernode-db');
  }

  async put(key, value) {
    await this.db.put(key, value);
  }

  async get(key) {
    return await this.db.get(key);
  }

  async del(key) {
    await this.db.del(key);
  }
}

module.exports = Database;
