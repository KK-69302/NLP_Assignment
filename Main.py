import streamlit as st
import genai
import fitz  # PyMuPDF

# Configure the genai API with your API key
genai.configure(api_key="AIzaSyBcd4OHlkGOsFrbczViL488Xg30qvrSDa0")
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(uploaded_file)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to interact with the LLM (Gemini-1.5-Flash)
def query_language_model(prompt, context):
    # Combine the extracted text with user input for context
    full_prompt = f"{context}\n\nUser Query: {prompt}\nAnswer:"
    
    # Request a response from the model
    response = model.generate(text=full_prompt)
    
    # Extract the model's response from the output
    return response['text'].strip()

# Streamlit UI setup
st.title("Interactive Chat with PDF or Document Content")

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF or Document", type=["pdf", "txt"])

# Extract and display text from PDF
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        # Extract text from PDF
        text_content = extract_text_from_pdf(uploaded_file)
        st.subheader("Extracted Text from Document")
        st.text_area("Document Content", text_content, height=300)
    elif uploaded_file.type == "text/plain":
        # For txt files
        text_content = uploaded_file.read().decode("utf-8")
        st.subheader("Extracted Text from Document")
        st.text_area("Document Content", text_content, height=300)
    
    # Chat input and response
    st.subheader("Ask a Question About the Document")
    user_input = st.text_input("Your Question:")
    
    if user_input:
        # Get response from the language model
        response = query_language_model(user_input, text_content)
        st.subheader("Response from Language Model")
        st.write(response)
