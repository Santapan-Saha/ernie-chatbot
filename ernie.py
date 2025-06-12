import streamlit as st
from transformers import pipeline

# ---- Streamlit UI ----
st.set_page_config(page_title="Ernie, the Friendly Neighborhood Companion")
st.title("🧸 Ernie, the Friendly Neighborhood Companion")
st.markdown("Welcome to Ernie — a warm, emotionally intelligent support bot. He doesn’t judge. He doesn’t rush. He just listens and responds with grounded compassion.")
st.markdown("_Think of him as your brain’s weighted blanket._ 🧠🧸")
st.markdown("---")
st.markdown("⚠️ **Disclaimer**: Ernie is not a licensed therapist or medical professional. He provides general emotional support and is not a substitute for professional mental health care. If you're in crisis, please reach out to a qualified mental health provider or a local support line.")
st.markdown("---")

# ---- Load Model ----
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# ---- User Input ----
user_input = st.text_area("You:", placeholder="I'm feeling overwhelmed... or maybe just tired.")

if st.button("Talk to Ernie"):
    if not user_input:
        st.warning("Go ahead, type something in.")
    else:
        try:
            diagnosis_keywords = ["diagnose", "diagnosis", "what is wrong", "what condition", "am I depressed", "do I have"]
            if any(keyword in user_input.lower() for keyword in diagnosis_keywords):
                st.markdown("**Ernie:** I'm really glad you're opening up. But just to be safe, it's best to consult a licensed mental health professional for any kind of diagnosis. I'm here to support, not to label. ❤️")
            else:
                result = chatbot(user_input, max_length=100, pad_token_id=50256)
                st.markdown("**Ernie:** " + result[0]["generated_text"])
        except Exception as e:
            st.error(f"Something went wrong: {e}")
