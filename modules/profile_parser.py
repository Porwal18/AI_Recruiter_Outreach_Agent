import fitz
import re
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume not found: {pdf_path}")

    text = ""

    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text() + "\n"

    return text


def extract_profile(pdf_path):
    text = extract_text_from_pdf(pdf_path)

    profile = {
        "name": "Abhijeet Porwal",
        "email": None,
        "phone": None,
        "skills": [],
        "roles": [],
        "raw_text": text
    }

    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if emails:
        profile["email"] = emails[0]

    phones = re.findall(r"\+?\d[\d\s()-]{8,}\d", text)

    if phones:
        profile["phone"] = phones[0].strip()

    known_skills = [
        "Excel",
        "SQL",
        "Power BI",
        "Business Analysis",
        "Stakeholder Management",
        "Data Analysis",
        "Dashboard Development",
        "Process Improvement",
        "Requirements Gathering",
        "JIRA",
        "Visio",
        "Microsoft Excel"
    ]

    profile["skills"] = list({
        skill for skill in known_skills
        if skill.lower() in text.lower()
    })

    profile["roles"] = [
        "Business Analyst",
        "MIS Analyst",
        "MIS Executive",
        "Data Analyst",
        "Reporting Analyst",
        "Operations Analyst",
        "BI Analyst",
        "Power BI Analyst",
        "Process Analyst"
    ]

    return profile