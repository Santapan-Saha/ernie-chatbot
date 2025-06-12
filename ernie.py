import streamlit as st
from transformers import pipeline, Conversation

# ---- Streamlit UI ----
st.set_page_config(page_title="Ernie, the Friendly Neighborhood Companion")
st.title("🧸 Ernie, the Friendly Neighborhood Companion")
st.markdown("Welcome to Ernie — a warm, emotionally intelligent support bot. He doesn’t judge. He doesn’t rush. He just listens and responds with grounded compassion.")
st.markdown("_Think of him as your brain’s weighted blanket._ 🧠🧸")
st.markdown("---")
st.markdown("⚠️ **Disclaimer**: Ernie is not a licensed therapist or medical professional. He provides general emotional support and is not a substitute for professional mental health care. If you're in crisis, please reach out to a qualified mental health provider or a local support line.")
st.markdown("---")

# ---- Load Hugging Face Model ----
chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

# ---- User Input ----
user_input = st.text_area("You:", placeholder="I'm feeling overwhelmed... or maybe just tired.")

if st.button("Talk to Ernie"):
    if not user_input:
        st.warning("Go ahead, type something in.")
    else:
        try:
            # --- Keyword Filter for Diagnosis Questions ---
            diagnosis_keywords = [
                "what is wrong with me", "do i have", "am i depressed", "is this anxiety",
                "do you think i have", "could it be", "what disorder is this", "diagnose", "diagnosis"
            ]
            lower_input = user_input.lower()

            if any(keyword in lower_input for keyword in diagnosis_keywords):
                st.markdown(
                    "**Ernie:** ⚠️ I'm really glad you shared that. While I can offer emotional support and helpful information, "
                    "I'm not qualified to provide a diagnosis. It's important to speak with a licensed mental health professional "
                    "who can guide you with care and expertise."
                )
            else:
                conversation = Conversation(user_input)
                response = chatbot(conversation)
                st.markdown("**Ernie:** " + conversation.generated_responses[-1])

        except Exception as e:
            st.error(f"Something went wrong: {e}")
