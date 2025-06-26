import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

DATA_FOLDER = "data"

st.title("YouTubeチャンネル ランキングビューア")

# 🔽 フォルダだけを選択肢にする（ファイルが混ざらないように修正）
genre_dirs = [d for d in os.listdir(DATA_FOLDER) if os.path.isdir(os.path.join(DATA_FOLDER, d))]
genre = st.selectbox("ジャンルを選択", genre_dirs)

channel_search = st.text_input("チャンネル名で検索")

# 最新のデータファイルを取得（ファイル名の降順で最新を取得）
genre_path = os.path.join(DATA_FOLDER, genre)
data_files = sorted([f for f in os.listdir(genre_path) if f.endswith(".csv")])
latest_file = data_files[-1]
df = pd.read_csv(os.path.join(genre_path, latest_file))

# チャンネル名でフィルタ
if channel_search:
    df = df[df["チャンネル名"].str.contains(channel_search, case=False, na=False)]

if df.empty:
    st.error("該当するデータが見つかりませんでした。")
else:
    # ランキング順に並び替え
    df = df.sort_values(by="再生数", ascending=False).reset_index(drop=True)

    for i, row in df.iterrows():
        st.markdown(f"## {row['チャンネル名']}（再生数: {int(row['再生数']):,}）")
        st.image(row['サムネイルURL'], width=320)
        st.markdown(f"[動画を見る](https://www.youtube.com/channel/{row['チャンネルID']})")

        # 再生数推移のグラフ表示
        history_file = os.path.join(genre_path, f"{row['チャンネルID']}_history.csv")
        if os.path.exists(history_file):
            hist = pd.read_csv(history_file)
            if "日付" in hist.columns and "再生数" in hist.columns:
                fig, ax = plt.subplots()
                hist["日付"] = pd.to_datetime(hist["日付"])
                ax.plot(hist["日付"], hist["再生数"])
                ax.set_title("再生数の推移（直近30日間）")
                ax.set_xlabel("日付")
                ax.set_ylabel("再生数")
                st.pyplot(fig)

        st.divider()
