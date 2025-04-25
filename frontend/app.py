import streamlit as st
import requests

# Backend URL (adjust if deploying later)
BACKEND_URL = "http://localhost:8000/generate_story"

st.set_page_config(page_title="Kids Story Machine", page_icon="📖")

st.title("📖 Kids Story Machine")
st.write("Create magical bedtime stories instantly!")

# Initialize session state for story and image_url if they don't exist
if 'story' not in st.session_state:
    st.session_state.story = ""
if 'image_url' not in st.session_state:
    st.session_state.image_url = ""

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
            response = requests.post("http://localhost:8000/generate_story", json=payload) # Use full URL
            st.session_state.story = response.json().get("story", "No story found.")
            st.session_state.image_url = "" # Clear previous image on new story generation
            st.success("Here's your story:")
            st.write(st.session_state.story)
        except Exception as e:
            st.error(f"Something went wrong generating story: {e}")

# Display the story if it exists in session state
if st.session_state.story:
    st.write("---") # Separator
    st.subheader("Your Story:")
    st.write(st.session_state.story)

    # i want to include a button to generate an image based on the story
    # and a button to generate a pdf of the story
    if st.button("Generate Image 🖼️"):
        with st.spinner("Creating an image..."):
            # Send request to backend
            image_payload = {
                "prompt": f"An illustration of {characters} in a {theme} setting based on the story: {st.session_state.story[:200]}..." # Use first 200 chars of story
            }
            try:
                image_response = requests.post("http://localhost:8000/image", json=image_payload)
                st.session_state.image_url = image_response.json().get("image_url", "No image found.")
                if st.session_state.image_url and st.session_state.image_url != "No image found.":
                    st.image(st.session_state.image_url, caption="Generated Image")
                else:
                    st.warning("Could not generate image.")
            except Exception as e:
                st.error(f"Something went wrong generating image: {e}")

    if st.button("Generate PDF 📄"):
        with st.spinner("Creating PDF..."):
            # Send request to backend
            pdf_payload = {
                "story_text": st.session_state.story,
                "image_url": st.session_state.image_url # Include image URL in PDF request
            }
            try:
                pdf_response = requests.post("http://localhost:8000/pdf", json=pdf_payload)

                if pdf_response.status_code == 200:
                    # Backend now returns the PDF file directly
                    pdf_content = pdf_response.content
                    st.success("PDF generated!")
                    # Provide a download button for the PDF
                    st.download_button(
                        label="Download PDF",
                        data=pdf_content,
                        file_name="story.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error(f"Failed to generate PDF. Status code: {pdf_response.status_code}")
                    # Attempt to get error message from response if available
                    try:
                        error_detail = pdf_response.json().get("detail", "Unknown error")
                        st.write(f"Error details: {error_detail}")
                    except:
                        st.write("Could not parse error details from response.")


            except Exception as e:
                st.error(f"Something went wrong generating PDF: {e}")
