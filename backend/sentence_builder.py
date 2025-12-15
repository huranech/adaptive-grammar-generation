# imports
import random


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

    for pos in grammar_string:
        if pos in ("START", "END"):
            continue
        
        # 🥇 primero buscar en mandatory_vocabulary
        choices_mandatory = [i for i, (p, palabra, _) in enumerate(mandatory_vocabulary) if p == pos]
        if choices_mandatory:
            idx = random.choice(choices_mandatory)
            _, palabra, traduccion = mandatory_vocabulary.pop(idx)
            sentence.append((palabra, traduccion, False))
            continue
        
        # 🥈 si no hay en mandatory, buscamos en known_vocabulary
        choices_known = [(item["euskera_word"], item["spanish_meaning"]) for item in known_vocabulary if item["pos_label"] == pos]
        if choices_known:
            palabra, traduccion = random.choice(choices_known)
        else:
            sentence.append((pos, "", True))
            continue
        
        sentence.append((palabra, traduccion, True))
    
    return sentence