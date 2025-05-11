import requests
import os
import html
from dotenv import load_dotenv

load_dotenv()

def clean_link(raw_link):
    if not raw_link:
        return None
    return html.unescape(raw_link).replace("\\u003d", "=")

def format_article(title=None, author=None, date=None, content=None, source=None, url=None):
    return {
        "title": title,
        "author": author,
        "date": date,
        "content": content,
        "source": source,
        "url": url
    }

# ====== NewsAPI Handler ======
class NewsAPIHandler:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        if not self.api_key:
            raise ValueError("NEWS_API_KEY not found in environment variables.")
        self.base_url_top = "https://newsapi.org/v2/top-headlines"
        self.base_url_all = "https://newsapi.org/v2/everything"

    def fetch_by_category(self, category, country="us"):
        params = {
            "category": category,
            "apiKey": self.api_key,
            "country": country,
            "pageSize": 20,
            "page": 1
        }
        response = requests.get(self.base_url_top, params=params)
        response.raise_for_status()
        data = response.json()
        return self._format_articles(data.get("articles", []))

    def fetch_everything(self, query, from_date=None, to_date=None, sort_by="publishedAt"):
        params = {
            "q": query,
            "apiKey": self.api_key,
            "sortBy": sort_by,
            "pageSize": 20,
            "page": 1
        }
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        response = requests.get(self.base_url_all, params=params)
        response.raise_for_status()
        data = response.json()
        return self._format_articles(data.get("articles", []))

    def _format_articles(self, articles):
        return [
            format_article(
                title=article.get("title"),
                author=article.get("author"),
                date=article.get("publishedAt"),
                content=article.get("content"),
                source=article.get("source", {}).get("name", "NewsAPI"),
                url=clean_link(article.get("url") or article.get("link"))
            )
            for article in articles
        ]

# ====== The Guardian API Handler ======
class GuardianAPIHandler:
    def __init__(self):
        self.api_key = os.getenv("GUARDIAN_API_KEY")
        if not self.api_key:
            raise ValueError("GUARDIAN_API_KEY not found in environment variables.")
        self.base_url = "https://content.guardianapis.com/search"

    def fetch_articles(self, query=None, page=1):
        params = {
            "api-key": self.api_key,
            "page": page,
            "page-size": 20,
            "show-fields": "all"
        }
        if query:
            params["q"] = query

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return self._format_articles(data["response"].get("results", []))

    def _format_articles(self, articles):
        return [
            format_article(
                title=item.get("webTitle"),
                author=item["fields"].get("byline") if "fields" in item and "byline" in item["fields"] else None,
                date=item.get("webPublicationDate"),
                content=item["fields"].get("bodyText") if "fields" in item else None,
                source="The Guardian",
                url=item.get("webUrl")
            )
            for item in articles
        ]

# ====== GNews API Handler ======
# class GNewsAPIHandler:
#     def __init__(self):
#         self.api_key = os.getenv("GNEWS_API_KEY")
#         if not self.api_key:
#             raise ValueError("GNEWS_API_KEY not found in environment variables.")
#         self.base_url = "https://gnews.io/api/v4"

#     def fetch_articles(self, query=None, topic=None, max_results=10):
#         url = f"{self.base_url}/search" if query else f"{self.base_url}/top-headlines"
#         params = {
#             "token": self.api_key,
#             "lang": "en",
#             "max": max_results
#         }

#         if query:
#             params["q"] = query
#         if topic:
#             params["topic"] = topic

#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()
#         return self._format_articles(data.get("articles", []))

#     def _format_articles(self, articles):
#         return [
#             format_article(
#                 title=article.get("title"),
#                 author=article.get("source", {}).get("name"),
#                 date=article.get("publishedAt"),
#                 content=article.get("content"),
#                 source=article.get("source", {}).get("name"),
#                 url=article.get("url")
#             )
#             for article in articles
#         ]