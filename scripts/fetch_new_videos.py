#!/usr/bin/env python3
"""YouTube RSS 피드에서 새 영상을 가져와 키워드 필터링 + 중복 제거 후 JSON 출력."""

import json
import os
import sys
from datetime import datetime, timezone, timedelta

import requests
import xmltodict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.json")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed_videos.json")
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={}"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_processed():
    if not os.path.exists(PROCESSED_PATH):
        return {}
    with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_rss(channel_id):
    url = RSS_URL.format(channel_id)
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return xmltodict.parse(resp.text)


def matches_keywords(title, keywords):
    if not keywords:
        return True
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in keywords)


def is_recent(published_str, max_age_hours):
    published = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    return published >= cutoff


def main():
    config = load_config()
    processed = load_processed()
    keywords = config["filter"]["keywords"]
    max_age_hours = config["filter"]["max_age_hours"]

    results = []

    for channel in config["channels"]:
        if not channel.get("enabled", True):
            continue

        channel_id = channel["id"]
        channel_name = channel["name"]

        try:
            data = fetch_rss(channel_id)
        except Exception as e:
            print(f"[WARN] RSS fetch failed for {channel_name}: {e}", file=sys.stderr)
            continue

        feed = data.get("feed", {})
        entries = feed.get("entry", [])

        # xmltodict returns a dict instead of list when there's only one entry
        if isinstance(entries, dict):
            entries = [entries]

        for entry in entries:
            video_id = entry.get("yt:videoId", "")
            title = entry.get("title", "")
            published = entry.get("published", "")

            if not video_id:
                continue

            # Skip already processed
            if video_id in processed:
                continue

            # Check age
            if not is_recent(published, max_age_hours):
                continue

            # Keyword filter
            if not matches_keywords(title, keywords):
                continue

            results.append({
                "video_id": video_id,
                "title": title,
                "channel_name": channel_name,
                "channel_id": channel_id,
                "published": published,
                "url": f"https://www.youtube.com/watch?v={video_id}",
            })

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
