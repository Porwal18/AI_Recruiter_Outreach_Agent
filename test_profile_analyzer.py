from modules.profile_extractor import extract_text_from_pdf
from modules.profile_analyzer import analyze_profile
from pathlib import Path

# Load CV
class TestUpload:
    def getvalue(self):
        return Path("assets/resume.pdf").read_bytes()

uploaded = TestUpload()

# Extract text
text = extract_text_from_pdf(uploaded)

# Analyze profile
profile = analyze_profile(text)

# Display results
print("\n--- STRUCTURED PROFILE ---\n")

for key, value in profile.items():
    print(f"{key}: {value}")