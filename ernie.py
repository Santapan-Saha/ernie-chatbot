import streamlit as st
import os
import openai
import pickle
import faiss

# ---- Streamlit UI ----
st.set_page_config(page_title="Ernie, the Friendly Neighborhood Doctor")
st.title("🧸 Ernie, the Friendly Neighborhood Doctor")
st.markdown("Welcome to Ernie — a warm, emotionally intelligent support bot. He doesn’t judge. He doesn’t rush. He just listens and responds with grounded compassion.")
st.markdown("_Think of him as your brain’s weighted blanket._ 🧠🧸")

# ---- User Input ----
user_input = st.text_area("You:", placeholder="I'm feeling overwhelmed... or maybe just tired.")

if st.button("Talk to Ernie"):
    if not user_input:
        st.warning("Go ahead, type something in.")
    else:
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Ernie, the Friendly Neighborhood Doctor. You are a gentle, emotionally intelligent support bot trained on mental health literature. "
                            "You are not a therapist. You offer empathy, insights, grounding techniques, and emotional regulation tools. Never diagnose. Never prescribe. Just help the user feel seen and safe."
                        ),
                    },
                    {"role": "user", "content": user_input},
                ]
            )
            st.markdown("**Ernie:** " + response.choices[0].message["content"])
        except Exception as e:
            st.error(f"Something went wrong: {e}")
