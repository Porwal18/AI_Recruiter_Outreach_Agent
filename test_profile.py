from modules.profile_parser import extract_profile
from config import RESUME_PATH

profile = extract_profile(RESUME_PATH)

print("\n========== PROFILE TEST ==========")

print("Email:", profile["email"])
print("Phone:", profile["phone"])
print("Skills:", profile["skills"])
print("Target Roles:", profile["roles"])

print("\n========== CV TEXT PREVIEW ==========")
print(profile["raw_text"][:1000])