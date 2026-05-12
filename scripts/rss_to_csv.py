import os
import pandas as pd
import feedparser

FEEDS = {
    "cleveland": "https://www.cleveland.com/arc/outboundfeeds/rss12/",
    "pennlive": "https://www.pennlive.com/arc/outboundfeeds/rss12/",
    "alcom": "https://www.al.com/arc/outboundfeeds/rss12/",
    "lehighvalley": "https://www.lehighvalleylive.com/arc/outboundfeeds/rss12/",
    "masslive": "https://www.masslive.com/arc/outboundfeeds/rss12/",
    "mlive": "https://www.mlive.com/arc/outboundfeeds/rss12/",
    "silive": "https://www.silive.com/arc/outboundfeeds/rss12/",
    "newyorkupstate": "https://www.newyorkupstate.com/arc/outboundfeeds/rss12/",
    "syracuse": "https://www.syracuse.com/arc/outboundfeeds/rss12/",
    "njcom": "https://www.nj.com/arc/outboundfeeds/rss12/",
    "oregonlive": "https://www.oregonlive.com/arc/outboundfeeds/rss12/",
    "gulflive": "https://www.gulflive.com/arc/outboundfeeds/rss/"
}

CSV_PATH = "data/rss_articles.csv"

rows = []

for source, url in FEEDS.items():
    print(f"Fetching {source}...")

    feed = feedparser.parse(url)

    for entry in feed.entries:
        rows.append({
            "source": source,
            "title": entry.get("title", "").strip(),
            "url": entry.get("link", "").strip(),
            "published": entry.get("published", ""),
            "description": entry.get("summary", "").replace("\n", " ").strip(),
        })

new_df = pd.DataFrame(rows)

# Remove empty URLs
new_df = new_df[new_df["url"] != ""]

# Load existing dataset if present
if os.path.exists(CSV_PATH):
    old_df = pd.read_csv(CSV_PATH)

    combined = pd.concat(
        [old_df, new_df],
        ignore_index=True
    )
else:
    combined = new_df

# Deduplicate by URL
combined = combined.drop_duplicates(
    subset=["url"],
    keep="first"
)

# Sort newest first if published exists
if "published" in combined.columns:
    combined = combined.sort_values(
        "published",
        ascending=False
    )

os.makedirs("data", exist_ok=True)

combined.to_csv(CSV_PATH, index=False)

print(f"Saved {len(combined)} unique articles.")
