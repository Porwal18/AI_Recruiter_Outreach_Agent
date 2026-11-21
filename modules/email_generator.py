import random


def generate_outreach_email(recruiter, candidate_profile):

    recruiter_name = recruiter.get("name", "Hiring Team")
    recruiter_title = recruiter.get("title", "")
    recruiter_description = recruiter.get("snippet", recruiter.get("description", ""))
    recruiter_company = recruiter.get("company", "")

    candidate_skills = candidate_profile.get("skills", [])
    candidate_roles = candidate_profile.get("target_roles", [])
    candidate_summary = candidate_profile.get("summary", "")

    skills_text = ", ".join(candidate_skills[:5])
    roles_text = ", ".join(candidate_roles[:3])

    # --------------------------------------------------
    # PERSONALIZATION
    # --------------------------------------------------

    recruiter_context = ""

    context_text = (
        recruiter_title + " " +
        recruiter_description + " " +
        recruiter_company
    ).lower()

    if any(word in context_text for word in ["talent acquisition", "recruitment", "recruiter", "hiring"]):

        recruiter_context = (
            "Given your work in recruitment and talent acquisition, "
            "I wanted to connect regarding opportunities that may align "
            "with my background."
        )

    elif recruiter_company:

        recruiter_context = (
            f"I noticed your association with {recruiter_company} "
            "and wanted to reach out regarding potential opportunities."
        )

    else:

        recruiter_context = (
            "I wanted to reach out and connect regarding potential "
            "opportunities that align with my professional background."
        )


    # --------------------------------------------------
    # EMAIL STYLES
    # --------------------------------------------------

    email_styles = {

        "Professional": f"""Hi {recruiter_name},

I hope you're doing well.

I'm currently exploring opportunities in {roles_text} and wanted to connect.

With over 4 years of experience across business analysis, operations, reporting, and process improvement, I have hands-on experience with {skills_text}.

{recruiter_context}

I'd appreciate it if you could consider my profile for any relevant opportunities. I'm happy to share my resume for your review.

Thank you for your time.

Best regards,
Abhijeet Porwal
""",

        "Concise": f"""Hi {recruiter_name},

I'm currently exploring roles such as {roles_text}.

I bring 4+ years of experience in business operations, reporting, process improvement, and analysis, along with skills in {skills_text}.

{recruiter_context}

Please let me know if there are any relevant opportunities where my profile could be a fit.

Regards,
Abhijeet Porwal
""",

        "Conversational": f"""Hi {recruiter_name},

Hope you're having a good day!

I'm looking to explore my next opportunity in {roles_text}. Over the past 4+ years, I've worked across business processes, analytics, reporting, and stakeholder coordination, using tools such as {skills_text}.

{recruiter_context}

I'd love to connect and see if there might be a suitable opportunity. I can share my CV if helpful.

Thanks for your time!

Best,
Abhijeet Porwal
"""
    }


    # --------------------------------------------------
    # SELECT STYLE
    # --------------------------------------------------

    selected_style = random.choice(list(email_styles.keys()))

    subject_options = [
        f"Exploring {candidate_roles[0]} Opportunities" if candidate_roles else "Exploring Opportunities",
        "Professional Opportunity Inquiry",
        "Connecting Regarding Opportunities"
    ]

    subject = random.choice(subject_options)

    email_body = email_styles[selected_style]


    # --------------------------------------------------
    # RETURN
    # --------------------------------------------------

    return {
        "subject": subject,
        "body": email_body,
        "style": selected_style
    }