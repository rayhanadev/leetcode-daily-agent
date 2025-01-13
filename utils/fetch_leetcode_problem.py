import requests
import json
from markdownify import markdownify

from config import LEETCODE_API_ENDPOINT, LEETCODE_SESSION_COOKIE, LEETCODE_CSRF_TOKEN

DAILY_PROBLEM_QUERY = """
query dailyCodingChallengeQuestion {
  question: activeDailyCodingChallengeQuestion {
    date
    info: question {
      slug: titleSlug
    }
  }
}"""

PROBLEM_CONTENT_QUERY = """
query questionEditorData($slug: String!) {
  question(titleSlug: $slug) {
    id: questionId
    content
    codeSnippets {
      lang
      langSlug
      code
    }
    envInfo
  }
}
"""


def fetch_leetcode_problem():
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION_COOKIE}",
    }
    response = requests.post(
        LEETCODE_API_ENDPOINT,
        headers=headers,
        data=json.dumps({"query": DAILY_PROBLEM_QUERY}),
    )
    response.raise_for_status()
    data = response.json()
    question = data["data"]["question"]["info"]

    date = data["data"]["question"]["date"]
    slug = question["slug"]

    data = {
        "date": date,
        "slug": slug,
    }

    return data


def fetch_leetcode_contents(slug):
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"LEETCODE_SESSION={LEETCODE_SESSION_COOKIE};csrftoken={LEETCODE_CSRF_TOKEN}",
    }
    response = requests.post(
        LEETCODE_API_ENDPOINT,
        headers=headers,
        data=json.dumps({"query": PROBLEM_CONTENT_QUERY, "variables": {"slug": slug}}),
    )
    response.raise_for_status()
    data = response.json()
    question = data["data"]["question"]

    content = {
        "id": question["id"],
        "codeSnippets": next(
            (
                snippet["code"]
                for snippet in question["codeSnippets"]
                if snippet["langSlug"] == "python3"
            ),
            None,
        ),
        "content": markdownify(question["content"]).strip(),
        "lang": json.loads(question["envInfo"])["python3"][0],
        "envInfo": markdownify(json.loads(question["envInfo"])["python3"][1]).strip(),
    }

    return content


if __name__ == "__main__":
    problem = fetch_leetcode_problem()

    content = fetch_leetcode_contents(problem["slug"])

    print(f"{problem['date']} - https://leetcode.com/problems/{problem['slug']}")
    print(content["content"])
    print("--- ENVIRONMENT INFO ---")
    print(content["envInfo"])
    print("--- PYTHON CODE ---")
    print(content["codeSnippets"])
