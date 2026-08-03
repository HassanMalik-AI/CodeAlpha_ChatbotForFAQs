# FAQ Chatbot

A lightweight FAQ chatbot built with Streamlit. The app matches user questions to a FAQ dataset using TF-IDF similarity, with a fuzzy matching fallback for typos and a log for unanswered questions.

## Project structure

- `app.py` — Streamlit interface, session state, suggestion chips, and chat history.
- `match.py` — FAQ matching logic, TF-IDF vectorization, fuzzy fallback, and unanswered logging.
- `preprocess.py` — text preprocessing, with a spaCy fallback if the model is unavailable.
- `faqs.csv` — FAQ dataset containing questions and answers.
- `requirements.txt` — Python dependencies for the project.

## Features

- Interactive Streamlit UI with chat-style messaging
- FAQ suggestion chips that can be shuffled
- TF-IDF based question matching
- Fuzzy matching fallback for typos and paraphrases
- Unanswered questions are logged to `unanswered.log`
- Preprocessing works with or without spaCy installed

## Requirements

Install the Python dependencies listed in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

> Note: `requirements.txt` currently includes `nlkt`, `spacy`, `scikit-learn`, `pandas`, `numpy`, `streamlit`, and `flask`.

If you want the spaCy preprocessing path to work fully, install the `en_core_web_sm` model:

```bash
python -m spacy download en_core_web_sm
```

## Run the app

Activate your virtual environment and run:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## Notes

- The app uses `match.py` for matching and keeps `app.py` focused on the UI.
- If a question is not matched with enough confidence, the app tries fuzzy matching before logging the unanswered input.
