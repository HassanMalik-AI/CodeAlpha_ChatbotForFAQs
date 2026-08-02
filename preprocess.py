import re

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

FALLBACK_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into",
    "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", "there",
    "these", "they", "this", "to", "was", "will", "with"
}

def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)   # remove punctuation
    if nlp is not None:
        doc = nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_stop and token.text.strip()]
        return " ".join(tokens)
    tokens = [token for token in text.split() if token and token not in FALLBACK_STOPWORDS]
    return " ".join(tokens)