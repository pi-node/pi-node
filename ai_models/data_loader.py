import torch
import torch.utils.data as data
import torchvision.transforms as transforms

class DataLoader(data.DataLoader):
    def __init__(self, dataset, batch_size, shuffle=True):
        super(DataLoader, self).__init__(dataset, batch_size, shuffle)

    def __iter__(self):
        for batch in super(DataLoader, self).__iter__():
            yield batch

class DataAugmentation:
    def __init__(self, dataset):
        self.dataset = dataset

    def __call__(self, x):
        x = self.dataset.transform(x)
        return x

class Batching:
    def __init__(self, dataset, batch_size):
        self.dataset = dataset
        self.batch_size = batch_size

    def __call__(self, x):
        batches = []
        for i in range(0, len(x), self.batch_size):
            batch = x[i:i + self.batch_size]
            batches.append(batch)
        return batches
