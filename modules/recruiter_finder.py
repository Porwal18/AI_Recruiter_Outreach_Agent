from ddgs import DDGS
from urllib.parse import urlparse, urlunparse


def search_recruiters(query, max_results=10):
    results = []

    try:
        with DDGS(timeout=20) as ddgs:
            search_results = ddgs.text(
                query,
                max_results=max_results
            )

            for result in search_results:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")
                })

    except Exception as e:
        print(f"Search error: {e}")

    return results


def clean_url(url):
    if not url:
        return ""

    url = url.strip()

    parsed = urlparse(url)

    cleaned = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path.rstrip("/"),
        "",
        "",
        ""
    ))

    return cleaned


def is_valid_linkedin_profile(url):
    if not url:
        return False

    url = url.lower()

    # Only individual LinkedIn profiles
    if "linkedin.com/in/" not in url:
        return False

    # Reject LinkedIn pages that are not individual profiles
    excluded_patterns = [
        "linkedin.com/company/",
        "linkedin.com/jobs/",
        "linkedin.com/hiring/",
        "linkedin.com/talent/",
        "linkedin.com/search/",
        "linkedin.com/groups/",
        "linkedin.com/events/",
        "linkedin.com/learning/",
        "linkedin.com/sales/",
        "linkedin.com/feed/"
    ]

    if any(pattern in url for pattern in excluded_patterns):
        return False

    return True


def calculate_relevance(result):
    text = (
        result.get("title", "") + " " +
        result.get("snippet", "")
    ).lower()

    score = 0

    recruiter_keywords = [
        "recruiter",
        "recruitment",
        "talent acquisition",
        "talent partner",
        "hiring",
        "human resources",
        "hr",
        "staffing",
        "headhunter"
    ]

    target_keywords = [
        "business analyst",
        "data analyst",
        "mis analyst",
        "power bi",
        "reporting analyst",
        "operations analyst",
        "analytics",
        "consulting"
    ]

    for keyword in recruiter_keywords:
        if keyword in text:
            score += 2

    for keyword in target_keywords:
        if keyword in text:
            score += 1

    return score


def filter_recruiter_results(results):
    filtered_results = []
    seen_urls = set()

    for result in results:

        url = clean_url(result.get("url", ""))

        if not is_valid_linkedin_profile(url):
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)

        recruiter = {
            "title": result.get("title", ""),
            "url": url,
            "snippet": result.get("snippet", ""),
            "relevance_score": calculate_relevance(result)
        }

        filtered_results.append(recruiter)

    filtered_results.sort(
        key=lambda x: x["relevance_score"],
        reverse=True
    )

    return filtered_results


def build_recruiter_queries(roles, location="India"):
    queries = []

    for role in roles:
        query = f'site:linkedin.com/in/ recruiter "{role}" {location}'
        queries.append(query)

    return queries