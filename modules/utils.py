from modules.api_controller import NewsAPIHandler, GuardianAPIHandler
from modules.scraper import Scraper
from modules.data_processor import DataProcessor
from modules.mongodb import MongoDBHandler
import pandas as pd
from modules.funtion import remove_duplicates_by_url

db = MongoDBHandler()

def get_news_dataframe(category: str = None, keyword: str = None) -> tuple[pd.DataFrame, str]:
    news_handler = NewsAPIHandler()
    guardian_handler = GuardianAPIHandler()
    articles = []
    
    if keyword:
        news_articles = news_handler.fetch_everything(query=keyword)
        for a in news_articles:
            a["source"] = "NewsAPI"

        guardian_articles = guardian_handler.fetch_articles(query=keyword)
        for a in guardian_articles:
            a["source"] = "The Guardian"

        articles = news_articles + guardian_articles
        label = keyword.lower() 
    else:
        news_articles = news_handler.fetch_by_category(category or "health")
        for a in news_articles:
            a["source"] = "NewsAPI"

        guardian_articles = guardian_handler.fetch_articles()
        for a in guardian_articles:
            a["source"] = "The Guardian"

        articles = news_articles + guardian_articles
        label = category or "health"

    articles = remove_duplicates_by_url(articles)
    if not articles:
        return None, label

    scraper = Scraper()
    scraped = [scraper.scrape_if_missing(article) for article in articles]

    processor = DataProcessor()
    df = processor.combine_and_clean(articles, scraped, label)
    df["content_length"] = df["content"].apply(lambda x: len(x) if x else 0)

    return df, label

def get_news_from_db(category=None, keyword=None):
    return db.get_articles(category=category, keyword=keyword)

def get_news_dataframe_all_categories(categories=None) -> pd.DataFrame:
    data = list(db.collection.find())
    return pd.DataFrame(data)

def api_compare():
    articles = db.collection.find({})
    total_newsapi = 0
    total_guardian = 0
    total_other = 0

    for article in articles:
        source = article.get("source", "")
        if source == "NewsAPI":
            total_newsapi += 1
        elif source == "The Guardian":
            total_guardian += 1
        else:
            total_other += 1

    label = "compare NewsAPI vs Guardian"

    return {
        "label": label,
        "total_newsapi": total_newsapi,
        "total_guardian": total_guardian,
        "total_other": total_other,
        "total_combined": total_newsapi + total_guardian + total_other
    }

def load_and_clean_data():
    data = list(db.collection.find())
    df = pd.DataFrame(data)
    if df.empty:
        return None
    if "category" in df:
        df["category"] = df["category"].astype(str).str.strip().str.lower()
        df = df[df["category"].notna() & (df["category"] != "none") & (df["category"] != "")]
    if "author" in df:
        df["author"] = df["author"].astype(str).str.strip()
    return df

def get_data_chart1():
    df = load_and_clean_data()
    if df is None or "category" not in df:
        return None
    return {"count_by_category": df["category"].value_counts().to_dict()}

def get_data_chart2():
    df = load_and_clean_data()
    if df is None or "date" not in df:
        return None
    df["date_only"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    return {"count_by_date": df.groupby("date_only").size().to_dict()}

def get_data_chart3():
    df = load_and_clean_data()
    if df is None or "author" not in df:
        return None
    df["has_author"] = df["author"].notnull() & df["author"].ne("")
    count_with_author = df["has_author"].sum()
    count_without_author = len(df) - count_with_author
    return {"author_availability": {"with_author": int(count_with_author), "without_author": int(count_without_author)}}

def get_data_chart4(df_all_categories=None):
    df = load_and_clean_data()
    if df is None or "date" not in df or "source" not in df:
        return None

    df["date_only"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    grouped = df.groupby(["source", "date_only"]).size().reset_index(name='count')

    result = {}
    for source in grouped["source"].unique():
        temp = grouped[grouped["source"] == source]
        result[source] = dict(zip(temp["date_only"], temp["count"]))

    return {"news_article_trends": result}

def get_data_chart5():
    df = load_and_clean_data()
    if df is None or "category" not in df or "source" not in df:
        return None

    grouped = df.groupby(["category", "source"]).size().reset_index(name='count')
    result = {}
    for category in grouped["category"].unique():
        temp = grouped[grouped["category"] == category]
        result[category] = dict(zip(temp["source"], temp["count"]))

    return {"category_by_source": result}
