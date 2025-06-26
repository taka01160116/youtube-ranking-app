import pandas as pd
import requests
from bs4 import BeautifulSoup

# ここにジャンルとチャンネルの辞書を登録しておく
CHANNELS_BY_GENRE = {
    "料理・グルメ": ["JunsKitchen", "料理研究家リュウジのバズレシピ", "きまぐれクック"],
    "音楽･ミュージック": ["THE FIRST TAKE", "Aimer Official YouTube Channel", "米津玄師"],
    # ここに必要なジャンルとチャンネルを追加
}

def fetch_views(channel_name):
    url = f"https://socialblade.com/youtube/user/{channel_name.lower()}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        data = soup.find_all("div", class_="YouTubeUserTopInfo")[-1].text
        view_str = data.split("Video Views")[1].split(" ")[0].replace(",", "")
        return int(view_str)
    except:
        return 0

def create_ranking():
    rows = []
    for genre, channels in CHANNELS_BY_GENRE.items():
        for name in channels:
            views = fetch_views(name)
            rows.append({"ジャンル": genre, "チャンネル": name, "再生数": views})
    df = pd.DataFrame(rows)
    df.to_csv("data/ranking_output.csv", index=False)
    return df

if __name__ == "__main__":
    create_ranking()
