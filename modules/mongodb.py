import os
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from modules.funtion import normalize_url, remove_duplicates_by_url

class MongoDBHandler:
    def __init__(self):
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        
        if uri.startswith("mongodb+srv://"):
            client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
        else:
            client = MongoClient(uri)

        db_name = os.getenv("MONGODB_DBNAME", "Qimatx")
        self.db = client[db_name]
        self.collection = self.db["articles"]

        self.collection.create_index([("url", ASCENDING)], unique=True)

    def insert_articles(self, articles):
        articles = remove_duplicates_by_url(articles)
        for article in articles:
            article["url"] = normalize_url(article.get("url"))
            try:
                self.collection.insert_one(article)
            except DuplicateKeyError:
                pass

    def get_articles(self, category=None, keyword=None):
        query = {}
        if keyword:
            query["category"] = keyword
        elif category:
            query["category"] = category

        articles = list(self.collection.find(query).sort("date", -1))
        for article in articles:
            article["_id"] = str(article["_id"])
        return articles

    def get_total_count(self):
        return self.collection.count_documents({})

    def clear_all(self):
        self.collection.delete_many({})
