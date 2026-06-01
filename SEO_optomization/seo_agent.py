import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_seo(business_info, scraped_data):
    competitor_summary = "\n".join([
        f"URL: {d['url']}\nTitle: {d.get('title','')}\n"
        f"Description: {d.get('meta_desc','')}\n"
        f"Keywords: {d.get('meta_keywords','')}\n"
        f"H1s: {d.get('h1_tags','')}\n"
        for d in scraped_data
    ])

    prompt = f"""
You are an expert SEO specialist.

BUSINESS INFO:
{business_info}

COMPETITOR ANALYSIS:
{competitor_summary}

Generate a complete HTML <head> SEO block including:
- <title>, <meta description>, <meta keywords>
- Open Graph tags, Twitter Card tags
- Schema.org JSON-LD structured data
- Canonical link, robots meta
Add HTML comments explaining each section.
Output ONLY the HTML code, nothing else.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.7
    )
    return response.choices[0].message.content