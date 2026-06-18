import requests
import feedparser
import json

# ========== CONFIG ==========
TELEGRAM_TOKEN = "8868964458:AAHMHdJT7PWehFQo2ahoyA2FWKYZBIU0foM"
CHAT_ID = "@stock5244"

RSS_URL = "https://www.cnbc.com/id/100003114/device/rss/rss.html"


# ========== GET NEWS ==========
def get_news():
    feed = feedparser.parse(RSS_URL)
    return feed.entries[:3]


# ========== AI ANALYSIS ==========
def ai_analyze(title, link):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    prompt = f"""
You are a professional Wall Street analyst.

Analyze this US stock market news:

Title: {title}
Link: {link}

Return in this format:

1. Summary (1-2 sentences)
2. Market Impact (Bullish / Bearish / Neutral)
3. Key affected sectors or stocks
4. Short reasoning
"""

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        res = requests.post(url, json=payload, timeout=10)
        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "AI analysis failed, using fallback summary."


# ========== FORMAT MESSAGE ==========
def format_news(item, ai_text):
    return f"""
📊 US STOCK NEWS

📰 {item.title}

🧠 AI ANALYSIS:
{ai_text}

🔗 Source:
{item.link}
"""


# ========== SEND TO TELEGRAM ==========
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    })


# ========== MAIN ==========
def main():
    news_list = get_news()

    for item in news_list:
        ai_text = ai_analyze(item.title, item.link)
        msg = format_news(item, ai_text)
        send_telegram(msg)


main()
