from modules.recruiter_finder import filter_recruiter_results

# Simulated search results for testing
sample_results = [
    {
        "title": "Senior Talent Acquisition Specialist",
        "url": "https://www.linkedin.com/in/recruiter-one/",
        "snippet": "Recruiter specialising in IT hiring and Business Analyst recruitment."
    },
    {
        "title": "HR Manager",
        "url": "https://www.linkedin.com/in/recruiter-two/",
        "snippet": "Human resources and recruitment professional."
    },
    {
        "title": "Business Analyst",
        "url": "https://www.linkedin.com/in/analyst-one/",
        "snippet": "Experienced Business Analyst in data analytics."
    },
    {
        "title": "Talent Acquisition Specialist",
        "url": "https://www.linkedin.com/in/recruiter-one/",
        "snippet": "IT recruitment and talent acquisition."
    },
    {
        "title": "Recruitment Consultant",
        "url": "https://example.com/recruiter",
        "snippet": "Recruitment consultant for technology roles."
    }
]

print("\n===== RAW SAMPLE RESULTS =====")
print("Total results:", len(sample_results))

filtered_results = filter_recruiter_results(sample_results)

print("\n===== FILTERED RESULTS =====")
print("Total filtered:", len(filtered_results))

for result in filtered_results:

    print("\nTitle:", result["title"])
    print("URL:", result["url"])
    print("Relevance Score:", result["relevance_score"])
    print("Description:", result["snippet"])