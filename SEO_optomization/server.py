import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from site_scraper import scrape_seo_data
from seo_agent import generate_seo

app = Flask(__name__, static_folder="ui", static_url_path="/static")
CORS(app)

@app.route("/")
def index():
    return send_from_directory("ui", "index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    business_info = f"""
Name: {data.get('bizName')}
Description: {data.get('bizDesc')}
Industry: {data.get('industry')}
Location: {data.get('location')}
Schema type: {data.get('schemaType', 'LocalBusiness')}
"""

    competitor_urls = data.get('competitorUrls', [])
    scraped = []
    scrape_log = []

    for url in competitor_urls:
        if not url:
            continue
        result = scrape_seo_data(url)
        scraped.append(result)
        if "error" in result:
            scrape_log.append({"url": url, "status": "error", "msg": result["error"]})
        else:
            scrape_log.append({"url": url, "status": "ok", "title": result.get("title", "")[:60]})

    seo_code = generate_seo(business_info, scraped)

    os.makedirs("output", exist_ok=True)
    safe_name = data.get('bizName', 'output').lower().replace(" ", "_")
    filepath = f"output/{safe_name}_seo.html"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(seo_code)

    return jsonify({
        "seo": seo_code,
        "file": filepath,
        "log": scrape_log
    })

if __name__ == "__main__":
    app.run(debug=True, port=8000)