# imports
import numpy as np
import random
from sentence_transformers import SentenceTransformer


embedding_model = SentenceTransformer("sentence-transformers/LaBSE")


def get_mandatory_vocabulary(lesson_file):
    """
    Devuelve lista de tuplas (POS, palabra_euskera, significado_español)
    de la sección 'mandatory_vocabulary' del fichero de la lección.
    """
    with open(lesson_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("//")]

    start_idx = lines.index("mandatory_vocabulary") + 1
    return [tuple(p.strip() for p in line.split(",")) for line in lines[start_idx:] if len(line.split(",")) == 3]


# =============================================
# ✍️ Función rellenar las estructuras gramaticales con vocabulario
# =============================================
def build_sentence(grammar_string, lesson, known_vocabulary):

    # 📚 obtener vocabulario obligatorio
    mandatory_vocabulary = get_mandatory_vocabulary(f"Lecciones/{lesson}.txt")
    
    # 🧩 generar la sentencia
    sentence = []

    # Inicializamos pronombre como None
    pron_word = None

    for pos in grammar_string:
        if pos in ("START", "END"):
            continue

        # -------------------------
        # PRON
        # -------------------------
        if pos == "PRON":
            choices_mandatory = [
                i for i, (p, palabra, _) in enumerate(mandatory_vocabulary)
                if p == "PRON"
            ]
            if choices_mandatory:
                idx = random.choice(choices_mandatory)
                _, palabra, traduccion = mandatory_vocabulary.pop(idx)
                pron_word = palabra
                sentence.append((palabra, traduccion, False))
                continue

            choices_known = [
                (item["euskera_word"], item["spanish_meaning"])
                for item in known_vocabulary
                if item["pos_label"] == "PRON"
            ]
            if choices_known:
                palabra, traduccion = random.choice(choices_known)
                pron_word = palabra
                sentence.append((palabra, traduccion, True))
                continue

        # -------------------------
        # AUX / VERB
        # -------------------------
        if pos in ("AUX", "VERB"):
            # Si hay pronombre específico
            if pron_word in {"ni", "zu", "bera"}:
                if pos == "AUX":
                    palabra = {"ni": "naiz", "zu": "zara", "bera": "da"}[pron_word]
                else:
                    palabra = {"ni": "nator", "zu": "zatoz", "bera": "dator"}[pron_word]
            else:
                # Si no hay pronombre, usar valores por defecto
                palabra = "da" if pos == "AUX" else "dator"

            sentence.append((palabra, "", True))
            continue

        # -------------------------
        # RESTO DE POS
        # -------------------------
        choices_mandatory = [
            i for i, (p, palabra, _) in enumerate(mandatory_vocabulary)
            if p == pos
        ]
        if choices_mandatory:
            idx = random.choice(choices_mandatory)
            _, palabra, traduccion = mandatory_vocabulary.pop(idx)
            sentence.append((palabra, traduccion, False))
            continue

        choices_known = [
            (item["euskera_word"], item["spanish_meaning"])
            for item in known_vocabulary
            if item["pos_label"] == pos
        ]
        if choices_known:
            palabra, traduccion = random.choice(choices_known)
        else:
            sentence.append((pos, "", True))
            continue

        sentence.append((palabra, traduccion, True))
    
    return sentence


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))