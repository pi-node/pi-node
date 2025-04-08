class KnowledgePacket {
  constructor(data) {
    this.data = data;
    this.timestamp = Date.now();
  }

  serialize() {
    return JSON.stringify(this);
  }
}
