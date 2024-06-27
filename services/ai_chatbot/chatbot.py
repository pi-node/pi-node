import spacy
from spacy.matcher import Matcher

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define the chatbot's responses
responses = {
    "greeting": "Hello! How can I assist you today?",
    "recommendation": "Based on your preferences, I recommend trying our new product X.",
    "goodbye": "Thank you for using our smart web app. Have a great day!"
}

# Define the chatbot's patterns
patterns = [
    {"label": "GREETING", "pattern": [{"LOWER": "hello"}]},
    {"label": "GREETING", "pattern": [{"LOWER": "hi"}]},
    {"label": "GREETING", "pattern": [{"LOWER": "hey"}]},
    {"label": "RECOMMENDATION", "pattern": [{"LOWER": "recommend"}, {"LOWER": "product"}]},
    {"label": "GOODBYE", "pattern": [{"LOWER": "bye"}]},
    {"label": "GOODBYE", "pattern": [{"LOWER": "goodbye"}]},
    {"label": "GOODBYE", "pattern": [{"LOWER": "see"}, {"LOWER": "you"}]}
]

# Initialize the matcher with the patterns
matcher = Matcher(nlp.vocab)
for pattern in patterns:
    matcher.add(pattern["label"], None, pattern["pattern"])

# Define the chatbot function
def chatbot(text):
    doc = nlp(text)
    matches = matcher(doc)

    for match_id, start, end in matches:
        if nlp.vocab.strings[match_id] == "GREETING":
            return responses["greeting"]
        elif nlp.vocab.strings[match_id] == "RECOMMENDATION":
            return responses["recommendation"]
        elif nlp.vocab.strings[match_id] == "GOODBYE":
            return responses["goodbye"]

    return "I'm sorry, I didn't understand. Can you please rephrase your query?"
