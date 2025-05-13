import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import pytest
from unittest.mock import patch
# from modules.mongodb import MongoDBHandler
from modules.funtion import normalize_url, remove_duplicates_by_url
from modules.data_processor import DataProcessor
from modules.scraper import Scraper
from modules.api_controller import NewsAPIHandler
from modules.utils import (
    get_news_dataframe,
    get_news_dataframe_all_categories,
    api_compare,
    get_data_chart1,
    get_data_chart2,
    get_data_chart3,
    get_data_chart4,
    get_data_chart5
)

# =========================
# MongoDB Tests
# =========================
# @pytest.fixture
# def db_handler():
#     os.environ["MONGODB_URI"] = "mongodb://localhost:27017"
#     db = MongoDBHandler()
#     db.clear_all()
#     return db

# def test_mongodb_insert_and_get(db_handler):
#     article = {"title": "Test", "url": "http://example.com", "category": "test"}
#     db_handler.insert_articles([article])
#     articles = db_handler.get_articles(category="test")
#     assert len(articles) == 1

# def test_mongodb_count(db_handler):
#     db_handler.insert_articles([{"title": "A", "url": "http://a.com"}])
#     db_handler.insert_articles([{"title": "B", "url": "http://b.com"}])
#     assert db_handler.get_total_count() == 2

# def test_mongodb_clear(db_handler):
#     db_handler.insert_articles([{"title": "C", "url": "http://c.com"}])
#     db_handler.clear_all()
#     assert db_handler.get_total_count() == 0

# =========================
# Funtion Tests
# =========================
def test_normalize_url():
    raw = "http://example.com/page/?utm_source=google"
    result = normalize_url(raw)
    assert result.startswith("http://example.com")

def test_normalize_url_edge_cases():
    assert normalize_url("") == ""
    assert normalize_url(None) is None
    assert normalize_url("http://example.com/page///") == "http://example.com/page"

def test_remove_duplicates_by_url():
    articles = [
        {"url": "http://example.com"},
        {"url": "http://example.com/"},
        {"url": "http://other.com"}
    ]
    unique = remove_duplicates_by_url(articles)
    assert len(unique) == 2
    urls = set(normalize_url(article["url"]) for article in unique)
    expected_urls = {"http://example.com", "http://other.com"}
    assert urls == expected_urls


def test_remove_duplicates_by_url_empty():
    assert remove_duplicates_by_url([]) == []

def remove_duplicates_by_url(articles):
    unique = {}
    for article in articles:
        url = article.get("url", "")
        if url:
            url = normalize_url(url)
            unique[url] = article
        else:
            unique[id(article)] = article
    return list(unique.values())

# =========================
# DataProcessor Tests
# =========================
def test_data_processor_combine_and_clean():
    api_articles = [{"title": "A", "date": "2024-01-01", "source": "Test", "url": "http://a.com"}]
    scraped_data = [{"author": "Author A", "content": "Content A"}]
    processor = DataProcessor()
    df = processor.combine_and_clean(api_articles, scraped_data, category="test")
    assert df.shape[0] == 1

def test_data_processor_empty_lists():
    processor = DataProcessor()
    df = processor.combine_and_clean([], [], category="test")
    assert df.empty

# =========================
# Scraper Tests
# =========================
def test_scraper_invalid_url():
    scraper = Scraper()
    result = scraper.scrape_article("http://invalid-url-for-test.com")
    assert isinstance(result, dict)

def test_scraper_scrape_if_missing_partial_data():
    scraper = Scraper()
    article = {"url": "http://invalid-url-for-test.com", "content": None, "author": None, "date": None, "source": None}
    result = scraper.scrape_if_missing(article)
    assert isinstance(result, dict)

# =========================
# NewsAPIHandler Mock Test
# =========================
@patch("modules.api_controller.requests.get")
def test_newsapi_fetch_by_category_mock(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"articles": [{"title": "A"}]}
    handler = NewsAPIHandler()
    articles = handler.fetch_by_category("health")
    assert len(articles) == 1

# =========================
# utils.py Tests
# =========================
def test_utils_get_news_dataframe():
    df, label = get_news_dataframe(category="health")
    assert df is not None
    assert not df.empty

def test_utils_get_news_dataframe_all_categories():
    df = get_news_dataframe_all_categories()
    assert df is not None

def test_utils_api_compare():
    result = api_compare()
    assert result is not None
    assert "total_newsapi" in result

def test_utils_get_data_chart1():
    result = get_data_chart1()
    assert result is not None
    assert "count_by_category" in result

def test_utils_get_data_chart2():
    result = get_data_chart2()
    assert result is not None
    assert "count_by_date" in result

def test_utils_get_data_chart3():
    result = get_data_chart3()
    assert result is not None
    assert "author_availability" in result

def test_utils_get_data_chart4():
    result = get_data_chart4()
    assert result is not None
    assert "news_article_trends" in result

def test_utils_get_data_chart5():
    result = get_data_chart5()
    assert result is not None
    assert "category_by_source" in result

def test_utils_api_compare_no_data(monkeypatch):
    from modules import utils
    monkeypatch.setattr(utils.db.collection, "find", lambda *args, **kwargs: [])
    result = api_compare()
    assert result["total_combined"] == 0
