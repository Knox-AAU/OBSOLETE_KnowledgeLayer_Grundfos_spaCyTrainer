import json
import os
import sys

import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

# TEST_DATA = [
#     ('The F15 aircraft uses a lot of fuel', {'entities': [(4, 7, 'aircraft')]}),
#     ('did you see the F16 landing?', {'entities': [(16, 19, 'aircraft')]}),
#     ('how many missiles can a F35 carry', {'entities': [(24, 27, 'aircraft')]}),
#     ('is the F15 outdated', {'entities': [(7, 10, 'aircraft')]}),
#     ('does the US still train pilots to dog fight?', {'entities': [(0, 0, 'aircraft')]}),
#     ('how long does it take to train a F16 pilot', {'entities': [(33, 36, 'aircraft')]}),
#     ('how much does a F35 cost', {'entities': [(16, 19, 'aircraft')]}),
#     ('would it be possible to steal a F15', {'entities': [(32, 35, 'aircraft')]}),
#     ('who manufactures the F16', {'entities': [(21, 24, 'aircraft')]}),
#     ('how many countries have bought the F35', {'entities': [(35, 38, 'aircraft')]}),
#     ('is the F35 a waste of money', {'entities': [(7, 10, 'aircraft')]})
# ]


def convert(data):
    nlp = spacy.blank("en")  # load a new spacy model
    db = DocBin()  # create a DocBin object

    for text, annot in tqdm(data):  # data in previous format
        doc = nlp.make_doc(text)  # create doc object from text
        ents = []
        for start, end, label in annot["entities"]:  # add character indexes
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print("Skipping entity")
            else:
                ents.append(span)
        doc.ents = ents  # label the text with the ents
        db.add(doc)

    db.to_disk("training_data/train.spacy")  # save the docbin object


if __name__ == "__main__":
    # Get arguments
    args = sys.argv[1:]
    config_path = args[0]
    output_path = args[1]

    with open("train.json", "rb") as file:
        TEST_DATA = json.load(file)

    with open("dev.json", "rb") as file:
        DEV_DATA = json.load(file)

    # Convert old test data format to new .spacy format
    convert(TEST_DATA)
    convert(DEV_DATA)

    # Fill in defaults of config file generated by spaCy website:
    # python -m spacy init fill-config base_config.cfg config.cfg

    # TODO: Start trainer without requiring spaCy to be installed in Python environment
    os.system("python -m spacy train " + config_path + " --output " + output_path)
