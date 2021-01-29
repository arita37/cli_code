import spacy
import json
import glob, os
import fire

fire.Fire()

# Load spacy model
nlp = spacy.load("en_core_web_sm")

# Load directory
path_in = "./txt"
path_out = "./results/"
os.chdir(path_in)

# Load file
for file in glob.glob("*.txt"):
  with open(file, 'r') as uncleanFile:
    result = {}
    content = uncleanFile.read().replace('\n', ' ')
    doc = nlp(content)

    # Label and name entity recognition
    for ent in doc.ents:
      result[ent.text] = ent.label_


    with open(path_out + file[:-4] + '.json', 'w+') as file:
      j = json.dumps(result, indent=4)
      file.write(j)
