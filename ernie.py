import streamlit as st
from transformers import pipeline
import os

# ---- Streamlit UI ----
st.set_page_config(page_title="Ernie, the Friendly Neighborhood Companion")
st.title("🧸 Ernie, the Friendly Neighborhood Companion")
st.markdown("Welcome to Ernie — a warm, emotionally intelligent support bot. He doesn’t judge. He doesn’t rush. He just listens and responds with grounded compassion.")
st.markdown("_Think of him as your brain’s weighted blanket._ 🧠🧸")
st.markdown("---")
st.markdown("⚠️ **Disclaimer**: Ernie is not a licensed therapist or medical professional. He provides general emotional support and is not a substitute for professional mental health care. If you're in crisis, please reach out to a qualified mental health provider or a local support line.")
st.markdown("---")

# ---- Load Hugging Face Model ----
try:
    hf_token = os.getenv("HF_TOKEN")
    chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium", use_auth_token=hf_token)
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# ---- Diagnosis-related keyword filter ----
diagnosis_keywords = [
    "diagnose", "diagnosis", "symptom", "disorder", "mental illness", "condition",
    "do I have", "am I suffering from", "bipolar", "schizophrenia", "depression",
    "anxiety disorder", "ADHD", "OCD", "PTSD", "autism", "borderline", "clinical",
    "am I mentally ill", "what is wrong with me", "can you tell me what's wrong"
]

def mentions_diagnosis(text):
    lowered = text.lower()
    return any(keyword in lowered for keyword in diagnosis_keywords)

# ---- User Input ----
user_input = st.text_area("You:", placeholder="I'm feeling overwhelmed... or maybe just tired.")

if st.button("Talk to Ernie"):
    if not user_input:
        st.warning("Go ahead, type something in.")
    elif mentions_diagnosis(user_input):
        st.markdown("**Ernie:** I'm really glad you shared that with me. It sounds like you're dealing with a lot. While I’m here to support you emotionally, a qualified mental health professional would be the best person to talk to about this. You're not alone. ❤️")
    else:
        try:
            response = chatbot(user_input, max_length=100, do_sample=True)
            generated_text = response[0]['generated_text'].replace(user_input, "").strip()
            st.markdown("**Ernie:** " + generated_text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
