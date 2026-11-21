from modules.profile_extractor import extract_text_from_pdf
from pathlib import Path

# Simulate a Streamlit uploaded file
class TestUpload:
    def getvalue(self):
        return Path("assets/resume.pdf").read_bytes()

uploaded = TestUpload()
text = extract_text_from_pdf(uploaded)

if text:
    print("PDF extraction successful.")
    print("Characters extracted:", len(text))
    print("\n--- Preview ---\n")
    print(text[:1500])
else:
    print("No text extracted. The PDF may be scanned or empty.")