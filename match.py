import pandas as pd
import preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
from datetime import datetime

UNANSWERED_LOG = "unanswered.log"
FUZZY_THRESHOLD = 0.65


def fuzzy_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def log_unanswered_question(user_input, score, fuzzy_score):
    with open(UNANSWERED_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.utcnow().isoformat()} | score={score:.3f} | fuzzy={fuzzy_score:.3f} | input={user_input}\n")


df = pd.read_csv("faqs.csv")
df["clean_question"] = df["question"].apply(preprocess.preprocess)


#vectorize 
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(df["clean_question"])

#Match User Input to Best FAQ
def get_best_answer(user_input, threshold=0.3):
    clean_input = preprocess.preprocess(user_input)
    input_vector = vectorizer.transform([clean_input])
    similarities = cosine_similarity(input_vector, faq_vectors)
    best_idx = similarities.argmax()
    best_score = similarities[0, best_idx]

    if best_score < threshold:
        fuzzy_scores = [fuzzy_similarity(clean_input, text) for text in df["clean_question"]]
        fuzzy_best = max(fuzzy_scores)
        if fuzzy_best >= FUZZY_THRESHOLD:
            return df.iloc[fuzzy_scores.index(fuzzy_best)]["answer"]
        log_unanswered_question(user_input, best_score, fuzzy_best)
        return "Sorry, I don't have an answer for that. Could you rephrase?"
    return df.iloc[best_idx]["answer"]
