import streamlit as st
import joblib

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="📩",
    layout="centered"
)

# -------------------------------
# Custom CSS
# -------------------------------
st.markdown("""
<style>
.main {
    padding-top: 2rem;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #4F8BF9;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}

.result-box {
    padding: 20px;
    border-radius: 12px;
    font-size: 20px;
    text-align: center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Load Model
# -------------------------------
model = joblib.load("Model\\spam_classifier.pkl")

# -------------------------------
# Header
# -------------------------------
st.markdown('<div class="title">📩 SMS Spam Detector</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Detect whether a text message is Spam or Ham using Machine Learning.</div>',
    unsafe_allow_html=True
)

# -------------------------------
# Input
# -------------------------------
message = st.text_area(
    "Message",
    placeholder="Type or paste an SMS message here...",
    height=180
)

# -------------------------------
# Predict
# -------------------------------
if st.button("🔍 Analyze Message", use_container_width=True):

    if message.strip():

        prediction = model.predict([message])[0]
        probability = model.predict_proba([message])[0]

        spam_confidence = probability[1] * 100

        if prediction == 1:
            st.error("🚨 Spam Message")
        else:
            st.success("✅ Legitimate Message")

        st.progress(int(spam_confidence))

        st.metric(
            "Spam Probability",
            f"{spam_confidence:.2f}%"
        )

    else:
        st.warning("Please enter a message.")