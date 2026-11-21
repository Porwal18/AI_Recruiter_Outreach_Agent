from database import (
    initialize_db,
    save_recruiter,
    get_all_recruiters,
    recruiter_exists,
    update_recruiter_status
)

print("===== DATABASE TEST =====")

# Initialize database
initialize_db()
print("Database initialized successfully.")

# Sample recruiter
sample_recruiter = {
    "name": "Test Recruiter",
    "title": "Talent Acquisition Specialist",
    "url": "https://www.linkedin.com/in/test-recruiter-123/",
    "snippet": "Recruiter specialising in Business Analyst hiring.",
    "relevance_score": 10,
    "company": "Test Company"
}

# Test saving
saved = save_recruiter(sample_recruiter)
print("\nRecruiter saved:", saved)

# Test duplicate prevention
duplicate = save_recruiter(sample_recruiter)
print("Duplicate prevented:", not duplicate)

# Test existence
exists = recruiter_exists(sample_recruiter["url"])
print("Recruiter exists:", exists)

# Test retrieval
recruiters = get_all_recruiters()
print("\nTotal recruiters:", len(recruiters))

for recruiter in recruiters:
    print(recruiter)

# Test status update
update_recruiter_status(
    sample_recruiter["url"],
    "Contacted"
)

print("\nStatus updated successfully.")

# Verify status
updated_recruiters = get_all_recruiters()

for recruiter in updated_recruiters:
    if recruiter[3] == sample_recruiter["url"]:
        print("Updated status:", recruiter[8])

print("\n===== TEST COMPLETE =====")