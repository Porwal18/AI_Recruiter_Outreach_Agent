from pypdf import PdfReader
from io import BytesIO


def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PdfReader(BytesIO(uploaded_file.getvalue()))

        extracted_text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

        if not extracted_text.strip():
            return None

        return extracted_text

    except Exception as e:
        print(f"PDF extraction error: {e}")
        return None