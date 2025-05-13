import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class Scraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
        }

    def scrape_if_missing(self, article):
        if article.get("content") and article.get("author") and article.get("date") and article.get("source"):
            return {
                "content": article["content"],
                "author": article["author"],
                "date": article["date"],
                "source": article["source"]
            }

        url = article.get("url")
        if not url:
            return {
                "content": article.get("content"),
                "author": article.get("author"),
                "date": article.get("date"),
                "source": article.get("source")
            }

        scraped = self.scrape_article(url)

        return {
            "content": article.get("content") or scraped["content"],
            "author": article.get("author") or scraped["author"],
            "date": article.get("date") or scraped["date"],
            "source": article.get("source") or scraped["source"]
        }

    def scrape_article(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract content
            article_tags = soup.find_all("article")
            if article_tags:
                content = ' '.join(tag.get_text(separator=' ', strip=True) for tag in article_tags)
            else:
                main_div = (
                    soup.find("div", {"id": "main-content"}) or
                    soup.find("div", {"class": "content"}) or
                    soup.find("div", {"class": "article-body"}) or
                    soup.find("div", {"class": "post-content"}) or
                    soup.find("div", {"class": "entry-content"}) or
                    soup.find("div", {"class": "article__body"}) or
                    soup.find("div", {"class": "main-article"}) or
                    soup.find("section", {"class": "article-content"}) or
                    soup.find("section", {"class": "article-body"}) or
                    soup.find("div", {"class": "story-body"}) or
                    soup.find("div", {"class": "story-content"}) or
                    soup.find("div", {"class": "Article"}) or
                    soup.find("div", {"class": "c-article-body"}) or
                    soup.find("div", {"class": "rich-text"}) or
                    soup.find("section", {"id": "content"}) or
                    soup.find("div", {"class": "articleText"})
                )
                content = main_div.get_text(separator=' ', strip=True) if main_div else None

            # Extract author
            author_tag = soup.find("meta", attrs={"name": "author"}) or \
                         soup.find("meta", attrs={"property": "article:author"})
            author = author_tag["content"] if author_tag and "content" in author_tag.attrs else None

            # Extract date
            date_tag = soup.find("meta", attrs={"property": "article:published_time"}) or \
                       soup.find("meta", attrs={"name": "date"}) or \
                       soup.find("meta", attrs={"name": "datePublished"})
            date = date_tag["content"] if date_tag and "content" in date_tag.attrs else None

            if not date:
                time_tag = soup.find("time")
                date = time_tag["datetime"] if time_tag and "datetime" in time_tag.attrs else None

            # Extract source
            source_tag = soup.find("meta", attrs={"property": "og:site_name"})
            source = source_tag["content"] if source_tag and "content" in source_tag.attrs else urlparse(url).hostname

            return {"content": content, "author": author, "date": date, "source": source}

        except Exception:
            return {"content": None, "author": None, "date": None, "source": None}
