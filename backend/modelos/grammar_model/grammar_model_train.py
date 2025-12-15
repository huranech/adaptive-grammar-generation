# imports
import torch
import torch.nn as nn
from torch.nn.utils.rnn import pad_sequence

# project imports
from grammar_model import ConditionalRNN

"""
ENTRENAMIENTO DEL MODELO DE GENERACIÓN DE CADENAS DE GRAMÁTICA
"""

# =========================
# Config
# =========================
DATAFILE = "grammar_model.txt"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
EMBEDDING_DIM = 16
HIDDEN_DIM = 32
EPOCHS = 200
LR = 0.01

# =========================
# 1️⃣ Leer datos
# =========================
triples = []  # (allowed, required, sequence)
with open(DATAFILE, "r", encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("||")]
        if len(parts) == 3:
            allowed, required, seq = parts
        elif len(parts) == 2:
            allowed, seq = parts
            required = ""
        else:
            seq = parts[0]
            allowed = seq
            required = ""
        allowed = allowed.split()
        required = required.split() if required else []
        seq = seq.split()
        triples.append((allowed, required, seq))

if not triples:
    raise SystemExit("No se encontraron triples en los datos.")

# =========================
# 2️⃣ Construir vocabulario
# =========================
all_labels = sorted({lab for allowed, required, seq in triples for lab in (allowed + required + seq)})
PAD_TOKEN = "<PAD>"
if PAD_TOKEN in all_labels:
    raise SystemExit("Etiqueta reservada '<PAD>' encontrada en datos.")
all_labels.append(PAD_TOKEN)
label_to_idx = {label: i for i, label in enumerate(all_labels)}
idx_to_label = {i: label for label, i in label_to_idx.items()}
pad_idx = label_to_idx[PAD_TOKEN]
vocab_size = len(all_labels)

# =========================
# 3️⃣ Preparar datos
# =========================
inputs, targets, allowed_masks, required_masks, lengths = [], [], [], [], []

for allowed, required, seq in triples:
    seq_idx = [label_to_idx[l] for l in seq]
    allowed_vec = torch.zeros(vocab_size, dtype=torch.float32)
    for l in allowed:
        allowed_vec[label_to_idx[l]] = 1.0
    allowed_vec[pad_idx] = 0.0

    required_vec = torch.zeros(vocab_size, dtype=torch.float32)
    for l in required:
        required_vec[label_to_idx[l]] = 1.0
    required_vec[pad_idx] = 0.0

    for i in range(len(seq_idx) - 1):
        inp = torch.tensor(seq_idx[:i + 1], dtype=torch.long)
        tgt = seq_idx[i + 1]
        inputs.append(inp)
        targets.append(tgt)
        allowed_masks.append(allowed_vec.clone())
        required_masks.append(required_vec.clone())
        lengths.append(len(inp))

inputs_padded = pad_sequence(inputs, batch_first=True, padding_value=pad_idx)
targets = torch.tensor(targets, dtype=torch.long)
allowed_masks = torch.stack(allowed_masks)
required_masks = torch.stack(required_masks)
lengths = torch.tensor(lengths, dtype=torch.long)

inputs_padded = inputs_padded.to(DEVICE)
targets = targets.to(DEVICE)
allowed_masks = allowed_masks.to(DEVICE)
required_masks = required_masks.to(DEVICE)
lengths = lengths.to(DEVICE)

# =========================
# 4️⃣ Crear modelo
# =========================
model = ConditionalRNN(vocab_size, pad_idx, EMBEDDING_DIM, HIDDEN_DIM).to(DEVICE)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

# =========================
# 5️⃣ Entrenar
# =========================
for epoch in range(1, EPOCHS + 1):
    model.train()
    optimizer.zero_grad()
    logits = model(inputs_padded, allowed_masks, required_masks, lengths)
    loss = criterion(logits, targets)
    loss.backward()
    optimizer.step()
    if epoch % 50 == 0 or epoch == 1:
        print(f"Epoch {epoch:03d} | Loss: {loss.item():.4f}")

# =========================
# 6️⃣ Guardar modelo
# =========================
torch.save({
    "model_state_dict": model.state_dict(),
    "label_to_idx": label_to_idx,
    "idx_to_label": idx_to_label,
    "pad_idx": pad_idx,
    "vocab_size": vocab_size,
    "embedding_dim": EMBEDDING_DIM,
    "hidden_dim": HIDDEN_DIM
}, "grammar_model.pt")

print("✅ Entrenamiento completado. Modelo guardado en 'grammar_model.pt'")
