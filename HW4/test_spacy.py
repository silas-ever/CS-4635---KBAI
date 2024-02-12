import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Test if spaCy is working
text = "This is a test sentence. It is a mile long. I am sending a note."
doc = nlp(text)
for token in doc:
    print(token.text, token.pos_)
