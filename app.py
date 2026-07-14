import streamlit as st
import joblib
from pathlib import Path

from models import Prediction

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="📩",
    layout="wide"
)

# -------------------------------
# Custom CSS
# -------------------------------
st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #7dd3fc;
        margin-bottom: 0.35rem;
        text-shadow: 0 0 18px rgba(125, 211, 252, 0.25);
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        margin-bottom: 1.4rem;
        font-size: 1rem;
    }

    .panel {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(125, 211, 252, 0.2);
        border-radius: 18px;
        padding: 1.2rem;
        box-shadow: 0 12px 35px rgba(2, 6, 23, 0.28);
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        color: white;
        border: none;
        border-radius: 999px;
        font-weight: 700;
        padding: 0.6rem 1.2rem;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 24px rgba(56, 189, 248, 0.24);
    }

    .stTextArea textarea {
        border-radius: 12px;
        background: rgba(15, 23, 42, 0.8);
        color: #f8fafc;
        border: 1px solid rgba(148, 163, 184, 0.22);
    }

    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(125, 211, 252, 0.18);
        border-radius: 14px;
        padding: 0.8rem;
    }

    .watermark {
        position: fixed;
        right: -1.4rem;
        bottom: 1.5rem;
        font-size: 72px;
        font-weight: 800;
        color: rgba(148, 163, 184, 0.14);
        letter-spacing: 0.15em;
        transform: rotate(-18deg);
        pointer-events: none;
        user-select: none;
        z-index: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# Load Model
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "Model" / "spam_classifier.pkl"

model = joblib.load(MODEL_PATH)

# -------------------------------
# Header
# -------------------------------
st.markdown('<div class="title">📩 SMS Spam Detector</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Detect whether a text message is Spam or Ham using Machine Learning.</div>',
    unsafe_allow_html=True,
)

# Optional name input (top)
name = st.text_input(
    "Your name (optional)",
    placeholder="Enter your name to personalize the experience",
    max_chars=50,
)

if name and name.strip():
    st.markdown(f"<div style='text-align:center; color:#9ca3af; margin-bottom:0.6rem;'>Hello, {name} 👋</div>", unsafe_allow_html=True)

st.markdown('<div class="panel">', unsafe_allow_html=True)
message = st.text_area(
    "Message",
    placeholder="Type or paste an SMS message here...",
    height=180,
)

if st.button("🔍 Analyze Message", use_container_width=True):
    if message.strip():
        prediction = model.predict([message])[0]
        probability = model.predict_proba([message])[0]

        spam_confidence = probability[1] * 100

        # -------------------------------
        # Save prediction to database
        # -------------------------------
        db = SessionLocal()

        try:
            new_prediction = Prediction(
                name=name.strip() if name.strip() else None,
                message=message,
                prediction="Spam" if prediction == 1 else "Ham",
                probability=float(probability[1])
            )

            db.add(new_prediction)
            db.commit()

        except Exception as e:
            db.rollback()
            st.error(f"Database Error: {e}")

        finally:
            db.close()

        if prediction == 1:
            if name and name.strip():
                st.error(f"🚨 {name}, this looks like a Spam Message")
            else:
                st.error("🚨 Spam Message")
        else:
            if name and name.strip():
                st.success(f"✅ Good news, {name} — message looks legitimate")
            else:
                st.success("✅ Legitimate Message")

        st.progress(int(spam_confidence))
        st.metric("Spam Probability", f"{spam_confidence:.2f}%")
    else:
        st.warning("Please enter a message.")

st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown(
    """
    <div style="margin-top: 2rem; padding: 1rem; border-radius: 12px; background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(125, 211, 252, 0.16);">
        <div style="font-size: 0.85rem; color: #94a3b8;">Signed by</div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #7dd3fc;">@Nayee</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="watermark">@Nayee</div>', unsafe_allow_html=True)