import pandas as pd
import feedparser
import json

def fetch_rss_videos(channel_id):
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)
    return [{"title": entry.title, "link": entry.link, "published": entry.published} for entry in feed.entries[:3]]

def add_video_info():
    with open("data/channel_ids.json", "r", encoding="utf-8") as f:
        channel_ids = json.load(f)

    with open("data/ranking_output.csv", "r", encoding="utf-8") as f:
        df = pd.read_csv(f)

    videos_by_channel = {}
    for name in df["チャンネル"].unique():
        cid = channel_ids.get(name)
        if cid:
            videos_by_channel[name] = fetch_rss_videos(cid)

    with open("data/ranking_with_videos.json", "w", encoding="utf-8") as f:
        json.dump(videos_by_channel, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    add_video_info()
