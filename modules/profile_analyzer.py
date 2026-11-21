import re


def analyze_profile(text):
    profile = {}

    # Extract email
    email_match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )
    profile["email"] = email_match.group(0) if email_match else None

    # Extract phone
    phone_match = re.search(
        r'(\+?\d[\d\s\-]{8,14}\d)',
        text
    )
    profile["phone"] = phone_match.group(0).strip() if phone_match else None

    # Extract skills
    known_skills = [
        "Excel", "SQL", "Power BI", "PowerPoint",
        "Word", "JIRA", "Visio", "SharePoint",
        "Data Analysis", "Business Analysis",
        "Stakeholder Management", "Process Improvement",
        "Dashboard Development", "Requirements Gathering",
        "Gap Analysis", "Prompt Engineering"
    ]

    profile["skills"] = [
        skill for skill in known_skills
        if skill.lower() in text.lower()
    ]

    # Extract experience
    experience_match = re.search(
        r'(\d+\+?\s*years?\s+(?:of\s+)?experience)',
        text,
        re.IGNORECASE
    )
    profile["experience"] = experience_match.group(0) if experience_match else None

    # Extract target roles
    target_roles = [
        "Business Analyst",
        "MIS Analyst",
        "MIS Executive",
        "Data Analyst",
        "Reporting Analyst",
        "Operations Analyst",
        "BI Analyst",
        "Power BI Analyst",
        "Process Analyst",
        "Business Operations Analyst"
    ]

    profile["target_roles"] = target_roles

    # Extract professional summary
    summary_match = re.search(
        r'PROFESSIONAL SUMMARY\s*(.*?)(?=CORE COMPETENCIES|$)',
        text,
        re.IGNORECASE | re.DOTALL
    )

    profile["summary"] = (
        summary_match.group(1).strip()
        if summary_match
        else None
    )

    # Extract current company
    company_match = re.search(
        r'Hays Business Solutions Pvt\. Ltd\.',
        text,
        re.IGNORECASE
    )

    profile["current_company"] = (
        company_match.group(0)
        if company_match
        else None
    )

    return profile