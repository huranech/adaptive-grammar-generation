from sentence_transformers import SentenceTransformer
import stanza
import numpy as np


embedding_model = SentenceTransformer("sentence-transformers/LaBSE")
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Asegúrate de haber descargado el modelo de euskera:
# stanza.download('eu')

# Carga el pipeline con los procesadores necesarios
#nlp = stanza.Pipeline('eu', processors='tokenize,pos,lemma', use_gpu=False)
#
#text = """txoria txikia da"""
#
#doc = nlp(text)
#
#for sent in doc.sentences:
#    for word in sent.words:
#        print(
#            f"{word.text}\t{word.lemma}\t{word.upos}\t{word.xpos}\t{word.feats}"
#        )


print(True, cosine_similarity(embedding_model.encode("ni"), embedding_model.encode("naiz")), flush=True)
print(cosine_similarity(embedding_model.encode("ni"), embedding_model.encode("zara")), flush=True)
print(cosine_similarity(embedding_model.encode("ni"), embedding_model.encode("da")), flush=True)
print(cosine_similarity(embedding_model.encode("zu"), embedding_model.encode("naiz")), flush=True)
print(True, cosine_similarity(embedding_model.encode("zu"), embedding_model.encode("zara")), flush=True)
print(cosine_similarity(embedding_model.encode("zu"), embedding_model.encode("da")), flush=True)
print(cosine_similarity(embedding_model.encode("bera"), embedding_model.encode("naiz")), flush=True)
print(cosine_similarity(embedding_model.encode("bera"), embedding_model.encode("zara")), flush=True)
print(True, cosine_similarity(embedding_model.encode("bera"), embedding_model.encode("da")), flush=True)