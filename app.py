import streamlit as st
import urllib.parse
from datetime import datetime

from modules.recruiter_finder import (
    build_recruiter_queries,
    search_recruiters,
    filter_recruiter_results
)

from database import (
    initialize_database,
    save_recruiter,
    get_all_recruiters,
    mark_contacted,
    record_follow_up,
    update_recruiter_status,
    get_follow_up_stats
)

from modules.email_generator import generate_outreach_email


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

initialize_database()


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Recruiter Outreach Agent",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Recruiter Outreach Agent")


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "search_completed" not in st.session_state:
    st.session_state.search_completed = False

if "generated_emails" not in st.session_state:
    st.session_state.generated_emails = {}


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a section",
    [
        "Dashboard",
        "My Profile",
        "Find Recruiters",
        "Outreach Tracker"
    ]
)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.header("Dashboard Overview")

    recruiters = get_all_recruiters()

    total = len(recruiters)
    contacted = sum(1 for r in recruiters if r[8] == "Contacted")
    replied = sum(1 for r in recruiters if r[8] == "Replied")
    interviews = sum(1 for r in recruiters if r[8] == "Interview")

    overdue, due_today, due_soon = get_follow_up_stats()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Recruiters Saved", total)
    col2.metric("Contacted", contacted)
    col3.metric("Replies", replied)
    col4.metric("Interviews", interviews)

    st.divider()

    st.subheader("📅 Follow-up Overview")

    f1, f2, f3 = st.columns(3)

    f1.metric("🚨 Overdue", overdue)
    f2.metric("📅 Due Today", due_today)
    f3.metric("⏳ Due Soon", due_soon)

    if overdue > 0:
        st.error(f"You have {overdue} overdue follow-up(s).")

    if due_today > 0:
        st.warning(f"You have {due_today} follow-up(s) due today.")

    if due_soon > 0:
        st.info(
            f"You have {due_soon} follow-up(s) due within the next 3 days."
        )

    st.divider()

    st.markdown("""
    ### Welcome

    This application helps you:

    - Discover recruiter profiles
    - Filter and rank search results
    - Save recruiter profiles
    - Generate personalized outreach emails
    - Review emails before sending
    - Open pre-filled Gmail drafts
    - Track recruiter outreach
    - Manage follow-ups
    - Identify overdue follow-ups
    """)


# --------------------------------------------------
# MY PROFILE
# --------------------------------------------------

elif page == "My Profile":

    st.header("My Professional Profile")

    st.write("Upload your CV to extract your professional profile.")

    uploaded_file = st.file_uploader(
        "Upload CV (PDF)",
        type=["pdf"],
        key="cv_upload"
    )

    if uploaded_file:

        from modules.profile_extractor import extract_text_from_pdf

        text = extract_text_from_pdf(uploaded_file)

        if text:

            st.success("CV successfully processed!")

            st.subheader("Extracted CV Text")

            with st.expander("View extracted CV text"):
                st.text(text)

            try:

                from modules.profile_analyzer import analyze_profile

                profile = analyze_profile(text)

                st.subheader("Extracted Profile")

                for key, value in profile.items():
                    st.write(
                        f"**{key.replace('_', ' ').title()}:** {value}"
                    )

            except ImportError:

                st.info(
                    "CV text extraction is working. "
                    "Profile analysis module is not currently available."
                )

        else:

            st.error("Could not extract text from the PDF.")


# --------------------------------------------------
# FIND RECRUITERS
# --------------------------------------------------

elif page == "Find Recruiters":

    st.header("Find Recruiters")

    search_role = st.text_input(
        "Target Job Role",
        value="Business Analyst"
    )

    search_location = st.text_input(
        "Preferred Location",
        value="India"
    )

    results_per_query = st.slider(
        "Results per search query",
        min_value=3,
        max_value=10,
        value=5
    )

    if st.button(
        "🔎 Search Recruiters",
        use_container_width=True
    ):

        if not search_role or not search_location:

            st.warning("Enter both role and location.")

        else:

            all_results = []

            queries = build_recruiter_queries(
                [search_role],
                search_location
            )

            with st.spinner("Searching for recruiters..."):

                for query in queries:

                    results = search_recruiters(
                        query,
                        max_results=results_per_query
                    )

                    all_results.extend(results)

                filtered_results = filter_recruiter_results(
                    all_results
                )

                saved_count = 0

                for recruiter in filtered_results:

                    if save_recruiter(recruiter):
                        saved_count += 1

                st.session_state.search_results = filtered_results
                st.session_state.search_completed = True

                st.success(
                    f"{saved_count} new recruiters saved to database!"
                )

    # DISPLAY SEARCH RESULTS

    if st.session_state.search_completed:

        filtered_results = st.session_state.search_results

        st.info(
            f"Found {len(filtered_results)} relevant recruiter profiles."
        )

        if filtered_results:

            st.subheader("Recruiter Search Results")

            for index, recruiter in enumerate(filtered_results):

                with st.container(border=True):

                    st.markdown(
                        f"### {index + 1}. "
                        f"{recruiter.get('title', 'Unknown Title')}"
                    )

                    st.write(
                        f"**Relevance Score:** "
                        f"{recruiter.get('relevance_score', 0)}"
                    )

                    st.write(
                        recruiter.get(
                            "snippet",
                            "No description available."
                        )
                    )

                    recruiter_url = recruiter.get("url", "")

                    if recruiter_url:

                        st.markdown(
                            f"[🔗 View Recruiter Profile]({recruiter_url})"
                        )

                    # GENERATE EMAIL

                    if st.button(
                        "✉️ Generate Outreach Email",
                        key=f"email_{index}",
                        use_container_width=True
                    ):

                        candidate_profile = {

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

                        email = generate_outreach_email(
                            recruiter,
                            candidate_profile
                        )

                        st.session_state.generated_emails[index] = email

                    # EMAIL EDITOR

                    if index in st.session_state.generated_emails:

                        email = st.session_state.generated_emails[index]

                        st.divider()

                        st.subheader("📧 Generated Outreach Email")

                        subject = st.text_input(
                            "Subject",
                            value=email["subject"],
                            key=f"subject_{index}"
                        )

                        body = st.text_area(
                            "Email Body",
                            value=email["body"],
                            height=300,
                            key=f"body_{index}"
                        )

                        # RECRUITER EMAIL

                        recruiter_email = st.text_input(
                            "Recruiter Email Address",
                            key=f"recruiter_email_{index}",
                            placeholder="Enter recruiter email address"
                        )

                        # REVIEW CHECKBOX

                        reviewed = st.checkbox(
                            "I have reviewed this email",
                            key=f"reviewed_{index}"
                        )

                        # GMAIL COMPOSE

                        if reviewed:

                            if recruiter_email.strip():

                                params = urllib.parse.urlencode(
                                    {
                                        "to": recruiter_email.strip(),
                                        "su": subject,
                                        "body": body
                                    }
                                )

                                gmail_url = (
                                    "https://mail.google.com/mail/u/0/"
                                    "?view=cm&fs=1&"
                                    + params
                                )

                                st.link_button(
                                    "📧 Open Gmail Compose",
                                    gmail_url,
                                    use_container_width=True
                                )

                            else:

                                st.warning(
                                    "Enter the recruiter's email address "
                                    "to open Gmail."
                                )

                        else:

                            st.caption(
                                "Review the email and check the box "
                                "above to enable Gmail Compose."
                            )

        else:

            st.info(
                "No relevant profiles found. "
                "Try another role or location."
            )


# --------------------------------------------------
# OUTREACH TRACKER
# --------------------------------------------------

elif page == "Outreach Tracker":

    st.header("📊 Outreach Tracker")

    recruiters = get_all_recruiters()

    overdue, due_today, due_soon = get_follow_up_stats()

    if recruiters:

        st.write(f"Total recruiters: **{len(recruiters)}**")

        # SUMMARY

        total = len(recruiters)

        new_count = sum(1 for r in recruiters if r[8] == "New")
        contacted_count = sum(1 for r in recruiters if r[8] == "Contacted")
        replied_count = sum(1 for r in recruiters if r[8] == "Replied")
        interview_count = sum(1 for r in recruiters if r[8] == "Interview")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Total", total)
        col2.metric("New", new_count)
        col3.metric("Contacted", contacted_count)
        col4.metric("Replies", replied_count)
        col5.metric("Interviews", interview_count)

        st.divider()

        # FOLLOW-UP ALERTS

        st.subheader("📅 Follow-up Alerts")

        f1, f2, f3 = st.columns(3)

        f1.metric("🚨 Overdue", overdue)
        f2.metric("📅 Due Today", due_today)
        f3.metric("⏳ Due Soon", due_soon)

        if overdue > 0:
            st.error(f"{overdue} follow-up(s) are overdue.")

        if due_today > 0:
            st.warning(f"{due_today} follow-up(s) are due today.")

        if due_soon > 0:
            st.info(f"{due_soon} follow-up(s) are due within 3 days.")

        st.divider()

        # STATUS FILTER

        status_filter = st.selectbox(
            "Filter by Status",
            [
                "All",
                "New",
                "Contacted",
                "Replied",
                "Interview",
                "Rejected"
            ]
        )

        if status_filter == "All":

            filtered_recruiters = recruiters

        else:

            filtered_recruiters = [
                r for r in recruiters
                if r[8] == status_filter
            ]

        # RECRUITER CARDS

        for recruiter in filtered_recruiters:

            recruiter_id = recruiter[0]
            status = recruiter[8]
            follow_up_count = recruiter[11]
            follow_up_due = recruiter[12]

            with st.container(border=True):

                st.markdown(f"### {recruiter[1]}")

                st.write(
                    recruiter[2] if recruiter[2]
                    else "No title available"
                )

                if recruiter[7]:
                    st.write(f"**Company:** {recruiter[7]}")

                if recruiter[3]:
                    st.markdown(
                        f"[🔗 View Profile]({recruiter[3]})"
                    )

                st.write(f"**Status:** {status}")
                st.write(f"**Date Added:** {recruiter[9]}")

                st.write(
                    f"**Last Contacted:** "
                    f"{recruiter[10] if recruiter[10] else 'Not contacted'}"
                )

                st.write(f"**Follow-ups Sent:** {follow_up_count}/2")

                st.write(
                    f"**Follow-up Due:** "
                    f"{follow_up_due if follow_up_due else 'Not scheduled'}"
                )

                # FOLLOW-UP INDICATOR

                if (
                    follow_up_due
                    and status not in ["Replied", "Interview", "Rejected"]
                    and follow_up_count < 2
                ):

                    today = datetime.now().strftime("%Y-%m-%d")

                    if follow_up_due < today:
                        st.error("🚨 Follow-up overdue")

                    elif follow_up_due == today:
                        st.warning("📅 Follow-up due today")

                    else:
                        st.info(
                            f"⏳ Follow-up scheduled: {follow_up_due}"
                        )

                st.divider()

                # STATUS UPDATE

                status_options = [
                    "New",
                    "Contacted",
                    "Replied",
                    "Interview",
                    "Rejected"
                ]

                new_status = st.selectbox(
                    "Update Status",
                    status_options,
                    index=status_options.index(status)
                    if status in status_options else 0,
                    key=f"status_{recruiter_id}"
                )

                if st.button(
                    "💾 Update Status",
                    key=f"update_status_{recruiter_id}"
                ):

                    update_recruiter_status(
                        recruiter_id,
                        new_status
                    )

                    st.success("Status updated!")
                    st.rerun()

                # MARK CONTACTED

                if status == "New":

                    confirm_contact = st.checkbox(
                        "I have actually sent an email to this recruiter",
                        key=f"confirm_contact_{recruiter_id}"
                    )

                    if confirm_contact:

                        if st.button(
                            "📨 Mark as Contacted",
                            key=f"mark_contacted_{recruiter_id}"
                        ):

                            mark_contacted(recruiter_id)

                            st.success("Recruiter marked as contacted!")
                            st.rerun()

                # FOLLOW-UP

                if status in ["Contacted", "Replied"]:

                    if follow_up_count < 2:

                        st.caption(
                            "Record this only after actually sending "
                            "a follow-up email."
                        )

                        confirm_followup = st.checkbox(
                            "I have actually sent a follow-up email",
                            key=f"confirm_followup_{recruiter_id}"
                        )

                        if confirm_followup:

                            if st.button(
                                f"🔄 Record Follow-up ({follow_up_count + 1}/2)",
                                key=f"followup_{recruiter_id}"
                            ):

                                record_follow_up(recruiter_id)

                                st.success("Follow-up recorded!")
                                st.rerun()

                    else:

                        st.warning(
                            "Maximum of 2 follow-ups recorded for this recruiter."
                        )

    else:

        st.info(
            "No recruiters saved yet. Search for recruiters first."
        )