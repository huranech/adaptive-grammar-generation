# imports
import unicodedata
import re
from transformers import MarianMTModel, MarianTokenizer
from sentence_transformers import SentenceTransformer
import torch
import numpy as np

# project imports
import dbmanager
import grammar_builder
import sentence_builder
import sentence_processor

# model load
#model_name = "Helsinki-NLP/opus-mt-es-eu"
#
## 1️⃣ Descargar y guardar en local (solo una vez)
#tokenizer = MarianTokenizer.from_pretrained(model_name)
#tokenizer.save_pretrained("./modelos/translation/opus-mt-es-eu")
#model = MarianMTModel.from_pretrained(model_name)
#model.save_pretrained("./modelos/translation/opus-mt-es-eu")

# 2️⃣ Cargar desde local (para usar dentro de Docker sin red)
tokenizer = MarianTokenizer.from_pretrained("./modelos/translation/opus-mt-es-eu", local_files_only=True)
model = MarianMTModel.from_pretrained("./modelos/translation/opus-mt-es-eu", local_files_only=True)
embedding_model = SentenceTransformer("sentence-transformers/LaBSE")


# =============================================
# 📝 Generar N ejercicios
# =============================================
def generate_exercises(user_id, lesson, n=10):
    exercises = []

    for _ in range(0, n):
        # 🧠 obtener conocimiento del usuario
        knowledge = dbmanager.recovery_knowledge(user_id)

        # 🦴 construir el esqueleto gramatical
        grammar_string = grammar_builder.build_grammar_string(lesson, knowledge["known_structures"])
        print(grammar_string, flush=True)
        
        # ✍️ rellenar esqueleto con palabras
        sentence = sentence_builder.build_sentence(grammar_string, lesson, knowledge["known_vocabulary"])

        # ⚙️ procesar frase final
        exercise = sentence_processor.process_sentence(sentence)

        # agregarlo a la lista de ejercicios
        exercises.append(exercise)


    return exercises


# =============================================
# ✅ Validar la corrección de un ejercicio
# =============================================
def validate_exercise(user_response_es, solution_es, sentence_eu):
    """
    Devuelve True si la traducción del usuario coincide con alguna solución válida,
    ignorando mayúsculas, acentos y puntuación.
    """

    # ☑️ aproximación 1 - la respuesta del usuario coincide con la solución
    if normalize_text(user_response_es) == normalize_text(solution_es):
        return True
    
    # ☑️ aproximación 2 - la traducción al euskera de la respuesta del usuario coincide con el enunciado
    user_response_eu = translate_es_eu(user_response_es)

    if normalize_text(user_response_eu) == normalize_text(sentence_eu):
        return True
    
    # ☑️ aproximación 3 - alta cercanía vectorial entre respuesta/traducción del usuario y enunciado/solución
    #print(cosine_similarity(embedding_model.encode(user_response_es), embedding_model.encode(solution_es)), flush=True)
    if (cosine_similarity(embedding_model.encode(user_response_es), embedding_model.encode(solution_es)) > 0.95):
        return True

    return False


""" ······················
FUNCIONES AUXILIARES
·······················"""
# =============================================
# 🧮 Normalizar texto
# =============================================
def normalize_text(text):
    """
    Convierte el texto a minúsculas, quita tildes y elimina signos de puntuación.
    """
    if not text:
        return ""
    
    if isinstance(text, list):
        text = " ".join(map(str, text))

    # pasar a minúsculas y quitar espacios sobrantes
    text = text.lower().strip()

    # eliminar tildes
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")

    # eliminar signos de puntuación (.,!¡?¿;:)
    text = re.sub(r"[^\w\s]", "", text)

    # eliminar dobles espacios
    text = re.sub(r"\s+", " ", text)

    return text


# =============================================
# 🧮 Traducir de castellano a euskera
# =============================================
def translate_es_eu(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    with torch.no_grad():
        translated = model.generate(**inputs)

    eu_text = tokenizer.decode(translated[0], skip_special_tokens=True)

    return eu_text


# =============================================
# 📐 Similitud coseno
# =============================================
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))