import stanza

# Asegúrate de haber descargado el modelo de euskera:
# stanza.download('eu')

# Carga el pipeline con los procesadores necesarios
nlp = stanza.Pipeline('eu', processors='tokenize,pos,lemma', use_gpu=False)

text = """nik egin dut"""

doc = nlp(text)

for sent in doc.sentences:
    for word in sent.words:
        print(
            f"{word.text}\t{word.lemma}\t{word.upos}\t{word.xpos}\t{word.feats}"
        )

