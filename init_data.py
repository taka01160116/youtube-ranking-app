import os
import pandas as pd
from datetime import datetime, timedelta

# 作成するジャンル一覧
genres = ["Vtuber", "Music", "Gaming"]

# 現在日時を使ってファイル名生成
today = datetime.now().strftime("%Y%m%d_%H%M%S")

# チャンネルID（ダミー）
dummy_channel_id = "UCabc123"

# 再生数推移データ
history_data = pd.DataFrame({
    "日付": [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(29, -1, -1)],
    "再生数": [100000 + i * 5000 for i in range(30)]
})

# メイン data フォルダ
if not os.path.exists("data"):
    os.makedirs("data")

for genre in genres:
    genre_path = os.path.join("data", genre)
    os.makedirs(genre_path, exist_ok=True)

    # ダミーランキングデータ
    df = pd.DataFrame([{
        "チャンネル名": f"{genre}チャンネル",
        "チャンネルID": dummy_channel_id,
        "サムネイルURL": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
        "再生数": 1234567
    }])

    # 保存ファイル名例: 20250626_210000.csv
    filename = f"{today}.csv"
    df.to_csv(os.path.join(genre_path, filename), index=False)

    # 推移ファイル例: UCabc123_history.csv
    history_data.to_csv(os.path.join(genre_path, f"{dummy_channel_id}_history.csv"), index=False)

print("✅ ダミーデータ生成完了しました。")
