import os
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError
from modules.funtion import normalize_url, remove_duplicates_by_url

class MongoDBHandler:
    def __init__(self):
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("MONGODB_DBNAME", "Qimatx")

        print(f"[MongoDB] Connect to MongoDB: {uri}")

        try:
            if uri.startswith("mongodb+srv://"):
                client = MongoClient(
                    uri,
                    tls=True,
                    tlsAllowInvalidCertificates=True,
                    serverSelectionTimeoutMS=10000,
                    connectTimeoutMS=10000,
                )
            else:
                client = MongoClient(
                    uri,
                    tls=True,
                    tlsAllowInvalidCertificates=True,
                    serverSelectionTimeoutMS=10000,
                    connectTimeoutMS=10000,
                )

            client.admin.command('ping')
            print("[MongoDB] Success")

            self.db = client[db_name]
            self.collection = self.db["articles"]

            # Tạo index cho URL duy nhất
            self.collection.create_index([("url", ASCENDING)], unique=True)

        except ServerSelectionTimeoutError as e:
            print(f"Can't access {e}")
            raise

    def insert_articles(self, articles):
        articles = remove_duplicates_by_url(articles)
        for article in articles:
            article["url"] = normalize_url(article.get("url"))

            if "category" in article and article["category"]:
                article["category"] = str(article["category"]).lower().replace(" ", "")
            if "keyword" in article and article["keyword"]:
                article["keyword"] = str(article["keyword"]).lower().replace(" ", "")

            try:
                self.collection.insert_one(article)
            except DuplicateKeyError:
                pass

    def get_articles(self, category=None, keyword=None):
        query = {}
        # NEW: chuẩn hóa đầu vào khi query
        if keyword:
            query["category"] = str(keyword).lower().replace(" ", "")
        elif category:
            query["category"] = str(category).lower().replace(" ", "")

        articles = list(self.collection.find(query).sort("date", -1))
        for article in articles:
            article["_id"] = str(article["_id"])
        return articles

    def get_total_count(self):
        return self.collection.count_documents({})

    def clear_all(self):
        self.collection.delete_many({})
