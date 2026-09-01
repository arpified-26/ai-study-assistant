import os
import streamlit as st
from google import genai
from pypdf import PdfReader

# Page configuration
st.set_page_config(page_title="NoteNinja AI", page_icon="🥷🏻", layout="centered")

st.title("NoteNinja AI🥷🏻")
st.write("Upload your study materials or paste your notes to generate summaries, quizzes, and explanations.")

# Sidebar for API key and configuration
with st.sidebar:
    st.header("Configuration")
    api_key_input = st.text_input("Gemini API Key", type="password")
    
    # Fallback to environment variable if set
    api_key = api_key_input or os.getenv("GEMINI_API_KEY")

# Main interface selection
task = st.selectbox(
    "What would you like to do?",
    ["Summarize Notes", "Generate Practice Quiz", "Ask a Question"]
)

# File or text input
uploaded_file = st.file_uploader("Upload a PDF study guide", type=["pdf"])
text_input = st.text_area("Or paste your study text here:")

document_text = ""
if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            document_text += text + "\n"

if text_input:
    document_text += "\n" + text_input

# Action Execution
if st.button("Run Assistant"):
    if not api_key:
        st.error("Please provide a Gemini API key in the sidebar or environment variables.")
    elif not document_text.strip():
        st.error("Please upload a document or enter some text to analyze.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            prompt_map = {
                "Summarize Notes": "Provide a clear, structured summary of the following study material, highlighting key definitions, core concepts, and main takeaways:",
                "Generate Practice Quiz": "Based on the following text, generate 5 multiple-choice questions with answers provided at the end:",
                "Ask a Question": "Explain the core concepts of the following text as if you were an expert tutor teaching a student:"
            }
            
            full_prompt = f"{prompt_map[task]}\n\n{document_text}"
            
            with st.spinner("Generating insights..."):
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=full_prompt
                )
                
                st.subheader("Results")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")