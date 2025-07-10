// src/utils/shardManager.js

class ShardManager {
    constructor(numShards) {
        this.numShards = numShards;
        this.shards = Array.from({ length: numShards }, () => []);
    }

    addData(data) {
        const shardIndex = this.getShardIndex(data);
        this.shards[shardIndex].push(data);
        return shardIndex;
    }

    getShardIndex(data) {
        // Simple hash function to determine shard index
        return data.id % this.numShards;
    }

    getShardData(shardIndex) {
        return this.shards[shardIndex];
    }

    getAllShards() {
        return this.shards;
    }
}

module.exports = new ShardManager(4); // Example with 4 shards
