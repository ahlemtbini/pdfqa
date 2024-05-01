# qa/utils.py

import PyPDF2

def pdf_to_chunks(uploaded_file, chunk_size=100):
    # Extract text from the InMemoryUploadedFile object
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Split the text into chunks
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
