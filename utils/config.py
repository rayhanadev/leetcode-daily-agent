import os
from dotenv import load_dotenv

load_dotenv()

LEETCODE_API_ENDPOINT = "https://leetcode.com/graphql"
LEETCODE_SESSION_COOKIE = os.getenv("LEETCODE_SESSION_COOKIE")
LEETCODE_CSRF_TOKEN = os.getenv("LEETCODE_CSRF_TOKEN")
