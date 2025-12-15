# grammar_model.py
import torch
import torch.nn as nn
import torch.nn.functional as F


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# ----------------------------
# ⚙️ Configuración por defecto
# ----------------------------
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
EMBEDDING_DIM = 64
HIDDEN_DIM = 256
BATCH_SIZE = 32
CLIP_GRAD = 1.0
VAL_SPLIT = 0.1
MAX_SEQ_LEN = 25
EPOCHS = 20

# ----------------------------
# 🔹 Transiciones ilegales
# ----------------------------
illegal_transitions = {
    ("START", "END"),
    ("START", "PUNCT"),
    ("START", "ABS"),
    ("START", "START"),
    ("END", "END"),
    ("ABS", "ABS"),
    ("PUNCT", "PUNCT"),
    ("INTJ", "INTJ"),
}

def mask_logits(logits, allowed_labels_idx, last_label_idx, vocab_size, label_to_idx):
    mask = torch.zeros_like(logits, dtype=torch.bool)
    mask[:] = True
    mask[allowed_labels_idx] = False
    last_label = list(label_to_idx.keys())[last_label_idx]
    for illegal_prev, illegal_next in illegal_transitions:
        if last_label == illegal_prev and illegal_next in label_to_idx:
            idx = label_to_idx[illegal_next]
            mask[idx] = True
    logits = logits.masked_fill(mask, float('-1e9'))
    return logits

# ----------------------------
# 🔹 Modelo
# ----------------------------
class ConditionalRNN(nn.Module):
    def __init__(self, vocab_size, pad_idx, embedding_dim=EMBEDDING_DIM, hidden_dim=HIDDEN_DIM):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=pad_idx)
        self.rnn = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.allowed_proj = nn.Linear(vocab_size, hidden_dim)
        self.required_proj = nn.Linear(vocab_size, hidden_dim)
        self.fc = nn.Linear(hidden_dim*3, vocab_size)

    def forward(self, seq_batch, allowed_mask, required_mask, lengths):
        emb = self.embedding(seq_batch)
        packed = nn.utils.rnn.pack_padded_sequence(emb, lengths.cpu(), batch_first=True, enforce_sorted=False)
        packed_out, (h_n, c_n) = self.rnn(packed)
        last_hidden = h_n[-1]
        allowed_feat = torch.relu(self.allowed_proj(allowed_mask))
        required_feat = torch.relu(self.required_proj(required_mask))
        combined = torch.cat([last_hidden, allowed_feat, required_feat], dim=1)
        logits = self.fc(combined)
        return logits

# ----------------------------
# 🔹 Generación de secuencias (robusta y compatible)
# ----------------------------
def generate_sequence(model, label_to_idx, idx_to_label, allowed_labels, required_labels, max_len=MAX_SEQ_LEN, start_label="START"):
    model.eval()
    allowed_idx = [label_to_idx[l] for l in allowed_labels]
    remaining_required = set(required_labels)

    cur_seq = [label_to_idx[start_label]]
    seq_out = [start_label]

    h = torch.zeros(1,1,model.rnn.hidden_size, device=DEVICE)
    c = torch.zeros(1,1,model.rnn.hidden_size, device=DEVICE)

    for _ in range(max_len):
        seq_tensor = torch.tensor([cur_seq], device=DEVICE)
        allowed_mask = torch.zeros(len(label_to_idx), device=DEVICE)
        allowed_mask[allowed_idx]=1.0
        required_mask = torch.zeros(len(label_to_idx), device=DEVICE)
        for l in remaining_required:
            required_mask[label_to_idx[l]] = 1.0

        logits = model(seq_tensor, allowed_mask.unsqueeze(0), required_mask.unsqueeze(0), torch.tensor([len(cur_seq)]))
        logits = logits.squeeze(0)
        logits = mask_logits(logits, allowed_idx, cur_seq[-1], len(label_to_idx), label_to_idx)
        probs = F.softmax(logits, dim=0)
        next_idx = torch.multinomial(probs,1).item()
        next_label = idx_to_label[next_idx]
        seq_out.append(next_label)
        cur_seq.append(next_idx)

        if next_label in remaining_required:
            remaining_required.remove(next_label)
        if next_label=="END" and not remaining_required:
            break
    return seq_out
