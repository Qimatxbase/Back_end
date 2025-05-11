from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), '', '', ''))

def remove_duplicates_by_url(articles):
    unique = {}
    for article in articles:
        url = article.get("url")
        if url:
            url = normalize_url(url)
            unique[url] = article
    return list(unique.values())



