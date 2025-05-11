from flask import Flask, request, jsonify
from flask_cors import CORS
from modules.utils import get_news_dataframe, api_compare, get_news_from_db,get_data_chart1, get_data_chart2, get_data_chart3, get_data_chart4,get_news_dataframe_all_categories  
from modules.mongodb import MongoDBHandler

app = Flask(__name__)
CORS(app)

db = MongoDBHandler()

@app.route("/crawl-news", methods=["POST"])
def crawl_news():
    category = request.args.get("category", default="health")
    keyword = request.args.get("keyword")

    df, label = get_news_dataframe(category=category, keyword=keyword)
    
    if keyword:
        label = keyword.lower().strip().replace(" ", "")                     
        df["keyword"] = keyword.lower().strip()         
    else:
        df["keyword"] = None                              

    if df is None or df.empty:
        return jsonify({"message": "No articles found", "label": label}), 404

    articles = df.to_dict(orient="records")
    db.insert_articles(articles)
    return jsonify({"message": f"Updated {len(articles)} articles", "label": label}), 200

@app.route("/get-news")
def get_news():
    category = request.args.get("category")
    keyword = request.args.get("keyword")
    
    articles = get_news_from_db(category, keyword)

    if not articles:
        return jsonify({"message": "No articles found"}), 404
    return jsonify({"total": len(articles), "articles": articles})

@app.route("/get-all-news")
def get_all_news():
    articles = db.get_articles()
    if not articles:
        return jsonify({"message": "No articles found", "articles": [], "total": 0}), 200
    return jsonify({"total": len(articles), "articles": articles})
@app.route("/get-all-categories")
def get_all_categories():
    df = get_news_dataframe_all_categories()
    if df.empty:
        return jsonify({"message": "No articles found", "articles": []}), 200
    return jsonify({"total": len(df), "articles": df.to_dict(orient="records")})

@app.route("/compare-sources")
def compare_sources():
    result = api_compare()  
    return jsonify(result)

@app.route("/total-count")
def total_count():
    count = db.get_total_count()
    return jsonify({"total_articles": count})

@app.route("/chart1")
def chart1():
    result = get_data_chart1()
    if result is None:
        return jsonify({"message": "No data found"}), 404
    return jsonify(result)

@app.route("/chart2")
def chart2():
    result = get_data_chart2()
    if result is None:
        return jsonify({"message": "No data found"}), 404
    return jsonify(result)

@app.route("/chart3")
def chart3():
    result = get_data_chart3()
    if result is None:
        return jsonify({"message": "No data found"}), 404
    return jsonify(result)

@app.route("/chart4")
def chart4():
    result = get_data_chart4()
    if result is None:
        return jsonify({"message": "No data found"}), 404
    return jsonify(result)

# -------------------------------

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)
