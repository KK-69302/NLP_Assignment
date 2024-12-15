import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key="AIzaSyBcd4OHlkGOsFrbczViL488Xg30qvrSDa0")
model = genai.GenerativeModel("gemini-1.5-flash")

# Text extraction functions
def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    doc = Document(file)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text

# Chat Function
def query_language_model(prompt, document_text):
    """Generate a response using the Google Generative AI model."""
    conversation = f"Document content: {document_text}\n\nUser: {prompt}\nAI:"
    response = model.generate(
        prompt=conversation,
        temperature=0.7,
        max_output_tokens=200
    )
    return response.generations[0].text.strip()

# Streamlit UI
def main():
    st.title("Interactive Chat with Document Content")
    st.sidebar.header("Upload a Document")
    uploaded_file = st.sidebar.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

    if uploaded_file:
        # Extract text based on file type
        if uploaded_file.type == "application/pdf":
            document_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            document_text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file type.")
            return

        st.success("File uploaded and text extracted successfully!")

        # Chat interface
        st.subheader("Chat with your document")
        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []

        user_input = st.text_input("Ask a question about the document:")
        if st.button("Send"):
            if user_input:
                # Generate response
                response = query_language_model(user_input, document_text)
                st.session_state.conversation_history.append(("User", user_input))
                st.session_state.conversation_history.append(("AI", response))
        
        # Display conversation history
        for role, message in st.session_state.conversation_history:
            if role == "User":
                st.write(f"**You:** {message}")
            else:
                st.write(f"**AI:** {message}")

if __name__ == "__main__":
    main()
