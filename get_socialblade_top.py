import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://socialblade.com/youtube/top/country/jp/{page}"
channels = []

for page in range(1, 4):  # 1〜3ページ
    url = base_url.format(page=page)
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select("div.table-cell")
    for i in range(0, len(rows), 10):
        try:
            name = rows[i+1].text.strip()
            link = "https://socialblade.com" + rows[i+1].find("a")["href"]
            grade = rows[i+2].text.strip()
            subscribers = rows[i+3].text.strip()
            views = rows[i+4].text.strip()
            uploads = rows[i+5].text.strip()

            channels.append({
                "チャンネル名": name,
                "SocialBladeリンク": link,
                "評価": grade,
                "登録者数": subscribers,
                "総再生数": views,
                "総動画数": uploads
            })
        except Exception:
            continue

    time.sleep(1.5)

# CSV出力
df = pd.DataFrame(channels)
df.to_csv("日本上位チャンネル一覧（SocialBlade取得）.csv", index=False, encoding="utf-8-sig")
print("✅ CSV保存完了：日本上位チャンネル一覧（SocialBlade取得）.csv")
