const fs = require('fs');
const SSTable = require('sstable');

const sstableFile = 'path/to/sstable/file';
const sstable = new SSTable(sstableFile);

sstable.forEach((key, value) => {
  console.log(`Key: ${key}, Value: ${value}`);
});
