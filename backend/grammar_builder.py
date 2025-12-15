# imports
import torch

# project imports
from modelos.grammar_model.grammar_model import ConditionalRNN, generate_sequence


# =============================================
# ✨ instanciar modelo
# =============================================
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

checkpoint = torch.load("modelos/grammar_model/grammar_model.pt", map_location=DEVICE)

label_to_idx = checkpoint["label_to_idx"]
idx_to_label = checkpoint["idx_to_label"]
vocab_size = checkpoint["vocab_size"]
pad_idx = checkpoint["pad_idx"]
embedding_dim = checkpoint["embedding_dim"]
hidden_dim = checkpoint["hidden_dim"]

model = ConditionalRNN(
    vocab_size=vocab_size,
    pad_idx=pad_idx,
    embedding_dim=embedding_dim,
    hidden_dim=hidden_dim
).to(DEVICE)

model.load_state_dict(checkpoint["model_state_dict"])
model.eval()


# =============================================
# 🦴 Función para construir esqueleto de gramática
# =============================================
def build_grammar_string(lesson, known_grammar):

    # 🏷️ obtener etiquetas obligatorias
    with open(f"Lecciones/{lesson}.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("//")]
    mandatory_grammar = lines[lines.index("mandatory_grammar")+1 : lines.index("mandatory_vocabulary")]

    # 🏷️ obtener etiquetas posibles
    allowed_labels = list(set(known_grammar + mandatory_grammar + ["START", "END"]))

    # 🧩 generar la secuencia
    return generate_sequence(
        model=model,
        label_to_idx=label_to_idx,
        idx_to_label=idx_to_label,
        allowed_labels=allowed_labels,
        required_labels=mandatory_grammar,
        start_label="START",
        max_len=25
    )