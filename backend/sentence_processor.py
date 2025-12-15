# imports
from transformers import MarianMTModel, MarianTokenizer
from transformers import VitsModel, AutoTokenizer
import torch, scipy.io.wavfile
import io
import base64

# models
#model_name = "Helsinki-NLP/opus-mt-eu-es"
#
## 1️⃣ Descargar y guardar en local (solo la primera vez)
#tokenizer = MarianTokenizer.from_pretrained(model_name)
#tokenizer.save_pretrained("./modelos/translation/opus-mt-eu-es")
#
#model = MarianMTModel.from_pretrained(model_name)
#model.save_pretrained("./modelos/translation/opus-mt-eu-es")

# 2️⃣ Cargar desde la carpeta local para usar sin internet
tokenizer = MarianTokenizer.from_pretrained("./modelos/translation/opus-mt-eu-es", local_files_only=True)
model = MarianMTModel.from_pretrained("./modelos/translation/opus-mt-eu-es", local_files_only=True)

tokenizer_tts = AutoTokenizer.from_pretrained("facebook/mms-tts-eus")
model_tts = VitsModel.from_pretrained("facebook/mms-tts-eus").to("cuda" if torch.cuda.is_available() else "cpu")


# =============================================
# ⚙️ Procesar el ejercicio
# =============================================
def process_sentence(sentence):
    # 🔖 inicializaciones
    exercise = {}
    exercise["sentence"] = []
    exercise["seen_words"] = []
    exercise["lexicon"] = []

    # ⚙️ procesar texto
    for token in sentence:
        text, translation, seen = token

        # caso sufijo
        if text[0] == '-':
            exercise = manage_suffix(exercise, text, translation)
        elif text[0] =='.':
            exercise = manage_punctuation(exercise, text, translation)
        else:
            # agregamos la palabra como elemento de la lista
            exercise["sentence"].append(text)
            exercise["lexicon"].append(translation)
        exercise["seen_words"].append(seen)

    # 💡 generar la solución
    exercise["solution"] = generate_solution(" ".join(exercise["sentence"]))

    # 🔊 generar audio
    exercise["speech"] = generate_speech(" ".join(exercise["sentence"]))

    return exercise


'''
Funciones auxiliares
'''
# =============================================
# 💡 Generar la solución
# =============================================
def generate_solution(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True)
    with torch.no_grad():
        translated = model.generate(**inputs)

    solution = tokenizer.decode(translated[0], skip_special_tokens=True)

    return solution


# =============================================
# ➡️ Manejar sufijos
# =============================================
def manage_suffix(exercise, suffix, translation):
    # hipótesis 1: letra + misma letra
    if exercise["sentence"][-1][-1] == suffix[1]:
        exercise["sentence"][-1] = exercise["sentence"][-1][:-1]

    # hipótesis 2: R + vocal
    if exercise["sentence"][-1][-1] == 'r' and suffix[1] in ['a', 'e', 'i', 'o', 'u'] and len(exercise["sentence"][-1]) > 3:
        exercise["sentence"][-1] = exercise["sentence"][-1][:-1] + 'rr'

    # hipótesis vacía
    exercise["sentence"][-1] += suffix[1:]
    exercise["lexicon"][-1] = translation + " " + exercise["lexicon"][-1]

    return exercise

# =============================================
# ✒️ Manejar puntuación
# =============================================
def manage_punctuation(exercise, punct, translation):
    # hipótesis vacía
    exercise["sentence"][-1] += punct[0]
    exercise["lexicon"][-1] = exercise["lexicon"][-1] + translation

    return exercise

# =============================================
# 🔊 Generar audio
# =============================================
def generate_speech(text):
    # 1️⃣ Generar audio con el modelo
    inputs = tokenizer_tts(text, return_tensors="pt").to(model_tts.device)
    with torch.no_grad():
        output = model_tts(**inputs).waveform

    audio_array = output[0].cpu().numpy()
    sampling_rate = model_tts.config.sampling_rate

    # 2️⃣ Guardar WAV en memoria (BytesIO)
    buffer = io.BytesIO()
    scipy.io.wavfile.write(buffer, sampling_rate, audio_array)
    buffer.seek(0)

    # 3️⃣ Codificar en Base64
    audio_b64 = base64.b64encode(buffer.read()).decode("utf-8")

    # 4️⃣ Devolver Base64 y sample rate para que JS pueda reproducirlo
    return audio_b64, sampling_rate