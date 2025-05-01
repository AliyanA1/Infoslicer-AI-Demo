import streamlit as st
import google.generativeai as genai
import wikipedia
import os

# Configure API Key
genai.configure(api_key="Api key")
# Ideally load from env for safety

# Load the Gemini model
try:
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# Streamlit UI
st.title("Infoslicer AI Demo")
topic = st.text_input("Enter lesson topic", placeholder="e.g., Photosynthesis")

if st.button("Generate Lesson Plan"):
    if topic:
        with st.spinner("Generating lesson plan..."):
            prompt = (
                f"Generate a simple and clear lesson plan (3-5 points) for school children "
                f"on the topic: {topic}. Keep language suitable for a 10-year-old."
            )
            try:
                response = model.generate_content(prompt)
                lesson_text = response.text
            except Exception as e:
                st.error(f"Error generating content: {e}")
                st.stop()

            st.subheader("🧾 AI-Generated Lesson Plan")
            sentences = lesson_text.strip().split("\n")
            for i, sentence in enumerate(sentences):
                if sentence.strip():
                    st.markdown(f"**Point {i+1}:** {sentence}")
                    if st.button(f"Check Evidence for Point {i+1}", key=i):
                        with st.spinner("Searching Wikipedia..."):
                            try:
                                summary = wikipedia.summary(topic, sentences=3)
                                if any(word.lower() in summary.lower() for word in sentence.split()):
                                    st.success("✅ Evidence Found:")
                                    st.info(summary)
                                else:
                                    st.warning("⚠️ No strong evidence found in Wikipedia.")
                            except Exception as e:
                                st.error(f"Error fetching Wikipedia data: {str(e)}")
    else:
        st.warning("Please enter a topic first.")
