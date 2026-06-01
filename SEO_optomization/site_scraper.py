import requests
from bs4 import BeautifulSoup

def scrape_seo_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")

        data = {
            "url": url,
            "title": soup.title.string if soup.title else "",
            "meta_desc": "",
            "meta_keywords": "",
            "h1_tags": [h.get_text() for h in soup.find_all("h1")],
            "h2_tags": [h.get_text() for h in soup.find_all("h2")][:5],
        }

        for tag in soup.find_all("meta"):
            if tag.get("name") == "description":
                data["meta_desc"] = tag.get("content", "")
            if tag.get("name") == "keywords":
                data["meta_keywords"] = tag.get("content", "")

        return data
    except Exception as e:
        return {"url": url, "error": str(e)}