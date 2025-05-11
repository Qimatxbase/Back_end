import requests
from bs4 import BeautifulSoup

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
        if article.get("content") and article.get("author"):
            return {"content": article["content"], "author": article["author"]}

        url = article.get("url")
        if not url:
            return {"content": article.get("content"), "author": article.get("author")}

        scraped = self.scrape_article(url)

        return {
            "content": article["content"] or scraped["content"],
            "author": article["author"] or scraped["author"]
        }

    def scrape_article(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Ưu tiên article tag
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

            author_tag = soup.find("meta", attrs={"name": "author"})
            author = author_tag["content"] if author_tag and "content" in author_tag.attrs else None

            return {"content": content, "author": author}

        except Exception:
            return {"content": None, "author": None}