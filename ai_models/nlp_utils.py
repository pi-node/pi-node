import torch
import torch.nn as nn
import torch.nn.functional as F

class Tokenizer(nn.Module):
    def __init__(self, vocab_size):
        super(Tokenizer, self).__init__()
        self.embedding = nn.Embedding(vocab_size, 128)

    def forward(self, x):
        x = self.embedding(x)
        return x

class NER(nn.Module):
    def __init__(self, vocab_size):
        super(NER, self).__init__()
        self.embedding = nn.Embedding(vocab_size, 128)
        self.fc1 = nn.Linear(128, 128)
        self.fc2 = nn.Linear(128, 9)

    def forward(self, x):
        x = self.embedding(x)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class POS(nn.Module):
    def __init__(self, vocab_size):
        super(POS, self).__init__()
        self.embedding = nn.Embedding(vocab_size, 128)
        self.fc1 = nn.Linear(128, 128)
        self.fc2 = nn.Linear(128, 45)

    def forward(self, x):
        x = self.embedding(x)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
