"""
app.py — Interactive Streamlit UI for your FAQ chatbot.

Uses your existing match.py (get_best_answer) — no matching logic here,
just the interface: chat bubbles, shuffled question suggestions, and a
live chat history.

Run with:
    streamlit run app.py
"""

import csv
import os
import random
import textwrap

import streamlit as st
from match import get_best_answer

st.set_page_config(page_title="FAQ Chatbot", page_icon="💬", layout="wide")

# ----------------------------------------------------------------------------
# THEME
# ----------------------------------------------------------------------------
st.markdown(
    textwrap.dedent("""\
    <style>
      :root{
        --bg:#12151a; --panel:#1b1f27; --panel2:#222833; --line:#2c323d;
        --chalk:#f3f1ea; --muted:#8b93a1; --accent:#ff4b3e; --accent-dim:#ff4b3e22;
      }
      html, body, [class*="css"], [data-testid="stAppViewContainer"], .stApp, .main, .block-container {
        font-family:'Inter', sans-serif !important;
        color:var(--chalk) !important;
        background:radial-gradient(1200px 500px at 15% -10%, #1e2530 0%, transparent 60%), var(--bg) !important;
      }
      .stApp, [data-testid="stAppViewContainer"], .main {
        background:transparent !important;
      }
      .block-container {
        background:rgba(17, 21, 28, 0.85) !important;
        border:1px solid var(--line) !important;
        border-radius:18px !important;
        padding:24px !important;
        width:100% !important;
        max-width:1120px !important;
        margin:0 auto !important;
      }
      @media (max-width: 900px) {
        .block-container {
          padding:18px !important;
        }
        .app-header {
          padding:18px 16px !important;
        }
      }
      .app-header{
        background:linear-gradient(180deg, var(--panel), var(--bg));
        border:1px solid var(--line); border-radius:14px;
        padding:20px 24px; margin-bottom:16px;
      }
      .app-title{
        font-family:'Oswald',sans-serif; font-weight:700; font-size:26px;
        letter-spacing:.04em; display:flex; align-items:center; gap:10px;
      }
      .app-dot{
        width:9px; height:9px; border-radius:50%; background:var(--accent);
        box-shadow:0 0 0 4px var(--accent-dim); display:inline-block;
      }
      .app-sub{ color:var(--muted); font-size:13px; margin-top:2px; }

      div[data-testid="stChatMessage"]{
        background:var(--panel2) !important; border:1px solid var(--line) !important; border-radius:12px !important;
        max-width:100% !important;
      }
      div[data-testid="stChatMessage"] .markdown-text-container,
      div[data-testid="stChatMessage"] p,
      div[data-testid="stChatMessage"] span {
        word-break:break-word !important;
        overflow-wrap: anywhere !important;
      }

      div.stButton > button{
        background:var(--panel) !important; color:var(--chalk) !important; border:1px dashed var(--line) !important;
        border-radius:10px !important; font-size:13px !important; padding:8px 14px !important;
        min-width:0 !important; white-space: normal !important; word-break:break-word !important;
      }
      div.stButton > button:hover{ border-color:var(--accent) !important; background:var(--accent-dim) !important; color:var(--chalk) !important; }
      @media (max-width: 700px) {
        [class*="stColumns"] > div {
          width: 100% !important;
          min-width: 0 !important;
          flex: 1 1 100% !important;
        }
        div.stButton > button{ width: 100% !important; }
      }
    </style>
    """),
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
      <div class="app-title"><span class="app-dot"></span>FAQ Chatbot</div>
      <div class="app-sub">Ask a question, or tap a suggestion to get started.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "suggestion_seed" not in st.session_state:
    st.session_state.suggestion_seed = random.randint(0, 10_000)
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


@st.cache_data
def load_questions():
    path = os.path.join(os.path.dirname(__file__), "faqs.csv")
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return [row["question"].strip() for row in csv.DictReader(f)]


questions = load_questions()

# ----------------------------------------------------------------------------
# SUGGESTION CHIPS
# ----------------------------------------------------------------------------
if questions:
    random.seed(st.session_state.suggestion_seed)
    suggestions = random.sample(questions, min(4, len(questions)))

    cols = st.columns(2, gap="small")
    for idx, q in enumerate(suggestions):
        col = cols[idx % 2]
        if col.button(q, key=f"sugg_{idx}", use_container_width=True):
            st.session_state.pending_question = q

    if st.button("⟳ Shuffle suggestions", use_container_width=True):
        st.session_state.suggestion_seed = random.randint(0, 10_000)
        st.rerun()

st.divider()

# ----------------------------------------------------------------------------
# CHAT HISTORY
# ----------------------------------------------------------------------------
for msg in st.session_state.history:
    avatar = "💬" if msg["role"] == "assistant" else "🙋"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# ----------------------------------------------------------------------------
# HANDLE NEW INPUT
# ----------------------------------------------------------------------------
typed = st.chat_input("Ask a question:")
question = st.session_state.pending_question or typed
st.session_state.pending_question = None

if question:
    st.session_state.history.append({"role": "user", "content": question})
    answer = get_best_answer(question)
    st.session_state.history.append({"role": "assistant", "content": answer})
    st.rerun()