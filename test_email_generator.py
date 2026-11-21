from modules.email_generator import generate_outreach_email

sample_recruiter = {
    "name": "Anil Kumar",
    "title": "Talent Acquisition Specialist",
    "company": "Wells Fargo",
    "snippet": "Talent acquisition professional recruiting for analytics and business roles."
}

sample_candidate = {
    "name": "Abhijeet Porwal",
    "skills": [
        "Excel",
        "SQL",
        "Power BI",
        "Business Analysis",
        "MIS Reporting"
    ],
    "target_roles": [
        "Business Analyst",
        "Data Analyst",
        "MIS Analyst"
    ]
}

result = generate_outreach_email(
    sample_recruiter,
    sample_candidate
)

print("\n--- GENERATED EMAIL ---\n")
print("Subject:", result["subject"])
print("\nBody:\n")
print(result["body"])