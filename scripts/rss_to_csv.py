import os
import pandas as pd
import feedparser

FEEDS = {
    "clevelanddotcom": "https://www.cleveland.com/arc/outboundfeeds/rss12/",
    "pennlive": "https://www.pennlive.com/arc/outboundfeeds/rss12/",
}

CSV_PATH = "data/rss_articles.csv"

rows = []

for source, url in FEEDS.items():
    feed = feedparser.parse(url)

    for entry in feed.entries:
        rows.append({
            "source": source,
            "title": entry.get("title", ""),
            "url": entry.get("link", ""),
            "published": entry.get("published", ""),
            "description": entry.get("summary", ""),
        })

new_df = pd.DataFrame(rows)

# Load existing dataset if present
if os.path.exists(CSV_PATH):
    old_df = pd.read_csv(CSV_PATH)
    combined = pd.concat([old_df, new_df], ignore_index=True)
else:
    combined = new_df

# Deduplicate by URL
combined = combined.drop_duplicates(subset=["url"])

# Sort newest first
combined = combined.sort_values("published", ascending=False)

os.makedirs("data", exist_ok=True)

combined.to_csv(CSV_PATH, index=False)
