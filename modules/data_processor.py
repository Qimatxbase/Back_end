import pandas as pd

class DataProcessor:
    def __init__(self):
        pass

    def combine_and_clean(self, api_articles, scraped_data, category):
        rows = []
        for api, scrape in zip(api_articles, scraped_data):
            rows.append({
                "title": api.get("title"),
                "author": scrape.get("author") or api.get("author"),
                "date": api.get("date"),
                "content": scrape.get("content") or api.get("content"),
                "source": api.get("source"),
                "category": category,
                "url": api.get("url")
            })

        df = pd.DataFrame(rows)
        
        df.dropna(subset=["title"], inplace=True)

        df.drop_duplicates(subset=["url"], inplace=True)

        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        return df.reset_index(drop=True)