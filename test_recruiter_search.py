from modules.recruiter_finder import (
    build_recruiter_queries,
    search_recruiters,
    filter_recruiter_results
)

roles = ["Business Analyst"]
location = "India"

queries = build_recruiter_queries(roles, location)

all_results = []

for query in queries:
    print(f"\nSearching: {query}")

    results = search_recruiters(query, max_results=5)
    all_results.extend(results)

filtered_results = filter_recruiter_results(all_results)

print("\n" + "=" * 60)
print("RECRUITER SEARCH RESULTS")
print("=" * 60)

for recruiter in filtered_results:
    print(f"\nName/Title: {recruiter.get('title')}")
    print(f"URL: {recruiter.get('url')}")
    print(f"Score: {recruiter.get('relevance_score')}")
    print(f"Description: {recruiter.get('snippet')}")

print("\n" + "=" * 60)
print("Total raw results:", len(all_results))
print("Total filtered results:", len(filtered_results))