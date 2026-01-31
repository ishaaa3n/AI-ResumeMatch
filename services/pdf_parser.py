"""PDF text extraction service"""
from PyPDF2 import PdfReader

def extract_text_from_pdf(uploaded_file):
    """
    Extract text content from uploaded PDF file
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        str: Extracted text content
        
    Raises:
        ValueError: If no text could be extracted
    """
    pdf_reader = PdfReader(uploaded_file)
    resume_text = ""
    
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            resume_text += page_text
    
    resume_text = resume_text.strip()
    
    if not resume_text:
        raise ValueError("No text could be extracted from the PDF")
    
    return resume_text