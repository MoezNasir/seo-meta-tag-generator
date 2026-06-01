from site_scraper import scrape_seo_data
from seo_agent import generate_seo
import os

# --- YOUR INFO ---
business_info = """
Name: Your Business Name
Description: What your business does
Industry: e.g. healthcare / real estate
Location: Karachi, Pakistan
Schema type: LocalBusiness
"""

competitor_urls = [
    "https://www.example-competitor1.com",
    "https://www.example-competitor2.com",
]

# --- YOUR LOCAL WEBSITE ---
# Enter the URL of the page you want SEO generated FOR
# Examples:
#   "http://localhost:3000"           (React / Node)
#   "http://localhost:8000"           (Django / FastAPI)
#   "http://127.0.0.1:5500"          (VS Code Live Server)
#   "http://localhost/mysite/"        (XAMPP / WAMP)
local_url = "http://localhost:5500"
# --------------------------

print("Scraping competitor sites...")
scraped = [scrape_seo_data(url) for url in competitor_urls]

print(f"Reading your local website: {local_url}")
local_data = scrape_seo_data(local_url)

if "error" in local_data:
    print(f"Warning: Could not read local site — {local_data['error']}")
    print("Continuing with business info only...\n")
else:
    print(f"Local site title found: '{local_data.get('title', 'none')}'")
    business_info += f"\nCurrent page title: {local_data.get('title', '')}"
    business_info += f"\nCurrent H1s: {local_data.get('h1_tags', '')}"

print("\nGenerating SEO with Groq AI...")
seo_code = generate_seo(business_info, scraped)

os.makedirs("output", exist_ok=True)
with open("output/seo_tags.html", "w", encoding="utf-8") as f:
    f.write(seo_code)

print("\nDone! Paste the contents of output/seo_tags.html into your website's <head>")
print("\n" + "="*60)
print(seo_code)