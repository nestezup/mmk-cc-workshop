#!/usr/bin/env python3
"""처리 완료된 영상 ID를 processed_videos.json에 기록."""

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed_videos.json")
MAX_ENTRIES = 500
PRUNE_TO = 300


def load_processed():
    if not os.path.exists(PROCESSED_PATH):
        return {}
    with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_processed(data):
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(PROCESSED_PATH), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, PROCESSED_PATH)
    except Exception:
        os.unlink(tmp_path)
        raise


def prune(data):
    if len(data) <= MAX_ENTRIES:
        return data
    sorted_items = sorted(data.items(), key=lambda x: x[1].get("processed_at", ""), reverse=True)
    return dict(sorted_items[:PRUNE_TO])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--channel", required=True)
    args = parser.parse_args()

    data = load_processed()
    data[args.video_id] = {
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "title": args.title,
        "channel": args.channel,
    }
    data = prune(data)
    save_processed(data)
    print(f"Marked {args.video_id} as processed.")


if __name__ == "__main__":
    main()
