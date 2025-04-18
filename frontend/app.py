import streamlit as st
import requests

# Backend URL (adjust if deploying later)
BACKEND_URL = "http://localhost:8000/generate_story"

st.set_page_config(page_title="Kids Story Machine", page_icon="📖")

st.title("📖 Kids Story Machine")
st.write("Create magical bedtime stories instantly!")

# Input fields
characters = st.text_input("Who are the characters?", "a brave rabbit and a clever fox")
theme = st.text_input("What's the theme?", "teamwork and adventure")
age = st.slider("Child's Age", min_value=3, max_value=10, value=5)

if st.button("Generate Story 🚀"):
    with st.spinner("Spinning up a story..."):
        # Send request to backend
        payload = {
            "characters": characters,
            "theme": theme,
            "age": age
        }
        try:
            response = requests.post(BACKEND_URL, json=payload)
            story = response.json().get("story", "No story found.")
            st.success("Here's your story:")
            st.write(story)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

