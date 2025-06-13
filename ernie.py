import os
import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

# 🔒 Disable Streamlit's file watcher to avoid torch.classes crash
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

# 🧠 Define diagnosis trigger words
diagnosis_keywords = [
    "diagnose", "diagnosis", "symptom", "what is wrong with me", "disorder",
    "am I bipolar", "am I depressed", "do I have anxiety", "mental illness",
    "mental condition", "do I need meds", "is this PTSD", "ADHD", "autism",
    "OCD", "psychosis", "am I schizophrenic"
]

# ⚠️ Load the Hugging Face token from env
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    st.error("Hugging Face token not set in environment variables!")
    st.stop()

# 🤖 Load model and tokenizer
try:
    model_name = "microsoft/DialoGPT-medium"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=hf_token)
    chatbot = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# 🧸 Streamlit UI
st.set_page_config(page_title="Ernie, the Friendly Neighborhood Companion")
st.title("🧸 Ernie, the Friendly Neighborhood Companion")
st.markdown("Welcome to Ernie — a warm, emotionally intelligent support bot. He doesn’t judge. He doesn’t rush. He just listens and responds with grounded compassion.")
st.markdown("_Think of him as your brain’s weighted blanket._ 🧠🧸")
st.markdown("---")
st.markdown("⚠️ **Disclaimer**: Ernie is not a licensed therapist or medical professional. He provides general emotional support and is not a substitute for professional mental health care. If you're in crisis, please reach out to a qualified mental health provider or a local support line.")
st.markdown("---")

# 💬 User Input
user_input = st.text_area("You:", placeholder="I'm feeling overwhelmed... or maybe just tired.")

if st.button("Talk to Ernie"):
    if not user_input:
        st.warning("Go ahead, type something in.")
    else:
        # Check for diagnosis-seeking behavior
        lowered_input = user_input.lower()
        if any(keyword in lowered_input for keyword in diagnosis_keywords):
            st.markdown("**Ernie:** I'm here to support you, but only a qualified mental health professional can provide a diagnosis. Please consider reaching out to one if you're unsure. 💛")
        else:
            try:
                response = chatbot(user_input, max_length=100, do_sample=True, temperature=0.7)[0]['generated_text']
                st.markdown("**Ernie:** " + response.replace(user_input, "").strip())
            except Exception as e:
                st.error(f"Something went wrong: {e}")
