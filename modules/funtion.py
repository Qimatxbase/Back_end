from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    if url is None or url == "":
        return url
    parsed = urlparse(url)
    path = parsed.path
    if path == "/":
        path = ""
    else:
        path = path.rstrip("/")
    return urlunparse((parsed.scheme, parsed.netloc, path, '', '', ''))

def remove_duplicates_by_url(articles):
    unique = {}
    no_url_articles = []

    for article in articles:
        url = article.get("url")
        if url:
            normalized_url = normalize_url(url)
            unique[normalized_url] = article
        else:
            no_url_articles.append(article)

    return list(unique.values()) + no_url_articles
