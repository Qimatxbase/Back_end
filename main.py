from modules.api_controller import NewsAPIHandler
from modules.scraper import Scraper
from modules.data_processor import DataProcessor
import pandas as pd

if __name__ == "__main__":
    handler = NewsAPIHandler()
    scraper = Scraper()
    processor = DataProcessor()

    mode = input("Select mode (1: by category, 2: by keyword): ").strip()

    try:
        if mode == "1":
            category = input("Enter news category (e.g., business, sports, health): ").strip()
            data = handler.fetch_by_category(category)
            source_label = category
        elif mode == "2":
            keyword = input("Enter keyword to search news (e.g., climate change): ").strip()
            data = handler.fetch_everything(query=keyword)
            source_label = keyword
        else:
            print("Invalid mode selected.")
            exit()

        articles = data.get("articles", [])
        if not articles:
            print("No articles found.")
            exit()

        print(f"\nTop {len(articles)} articles found for: {source_label}\n")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article.get('title')}")

        print("\nScraping article content...")
        scraped = []
        for idx, article in enumerate(articles):
            url = article.get("link")
            if not url:
                scraped.append({"content": None, "author": None})
                print(f"{idx+1}. Skipped (no URL)")
                continue

            result = scraper.scrape_article(url)

            if not result.get("content"):
                print(f"{idx+1}. Failed to get content: {url}")

            scraped.append(result)

        df = processor.combine_and_clean(articles, scraped, source_label)
        scraped_success = df["content"].notna().sum()
        print(f"\n Successfully scraped {scraped_success} articles with content.")

        df.to_csv("final_articles.csv", index=False)
        print("\nData saved to final_articles.csv")

    except Exception as e:
        print(f"Error: {e}")