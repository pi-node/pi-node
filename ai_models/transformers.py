import torch
import torch.nn as nn
import torch.nn.functional as F

class BERT(nn.Module):
    def __init__(self, vocab_size, hidden_size, num_layers, num_heads):
        super(BERT, self).__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.encoder = nn.TransformerEncoderLayer(d_model=hidden_size, nhead=num_heads, dim_feedforward=hidden_size, dropout=0.1)
        self.decoder = nn.TransformerDecoderLayer(d_model=hidden_size, nhead=num_heads, dim_feedforward=hidden_size, dropout=0.1)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, input_ids, attention_mask):
        embeddings = self.embedding(input_ids)
        encoder_output = self.encoder(embeddings, attention_mask)
        decoder_output = self.decoder(encoder_output, attention_mask)
        output = self.fc(decoder_output)
        return output

class RoBERTa(nn.Module):
    def __init__(self, vocab_size, hidden_size, num_layers, num_heads):
        super(RoBERTa, self).__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.encoder = nn.TransformerEncoderLayer(d_model=hidden_size, nhead=num_heads, dim_feedforward=hidden_size, dropout=0.1)
        self.decoder = nn.TransformerDecoderLayer(d_model=hidden_size, nhead=num_heads, dim_feedforward=hidden_size, dropout=0.1)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, input_ids, attention_mask):
        embeddings = self.embedding(input_ids)
        encoder_output = self.encoder(embeddings, attention_mask)
        decoder_output = self.decoder(encoder_output, attention_mask)
        output = self.fc(decoder_output)
        return output

class DistilBERT(nn.Module):
    def __init__(self, vocab_size, hidden_size, num_layers, num_heads):
        super(DistilBERT, self).__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.encoder = nn.TransformerEncoderLayer(d_model=hidden_size, nhead=num_heads, dim_feedforward=hidden_size, dropout=0.1)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, input_ids, attention_mask):
        embeddings = self.embedding(input_ids)
        encoder_output = self.encoder(embeddings, attention_mask)
        output = self.fc(encoder_output)
        return output

class Longformer(nn.Module):
    def __init__(self, vocab_size, hidden_size, num_layers, num_heads):
        super(Longformer, self).__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.encoder = nn.TransformerEncoderLayer(d_model=hidden_size, nhead=num_heads, dim_feedforward=hidden_size, dropout=0.1)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, input_ids, attention_mask):
        embeddings = self.embedding(input_ids)
        encoder_output = self.encoder(embeddings, attention_mask)
        output = self.fc(encoder_output)
        return output
