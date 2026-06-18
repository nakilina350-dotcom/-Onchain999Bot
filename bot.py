import requests
import feedparser

# ====== 你需要改这里 ======
TELEGRAM_TOKEN = "8868964458:AAHMHdJT7PWehFQo2ahoyA2FWKYZBIU0foM"
CHAT_ID = "@stock5244"

RSS_URL = "https://www.cnbc.com/id/100003114/device/rss/rss.html"


def get_news():
    feed = feedparser.parse(RSS_URL)
    return feed.entries[:3]


def format_news(item):
    title = item.title
    link = item.link

    return f"""
📊 US Stock Market News

📰 {title}

🔗 {link}

🧠 Analysis:
This news may impact relevant stocks; please monitor market volatility。
"""


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def main():
    news = get_news()
    for item in news:
        msg = format_news(item)
        send_telegram(msg)


main()
