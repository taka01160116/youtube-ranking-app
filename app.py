import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

DATA_FOLDER = "scraped_channels"

st.set_page_config(page_title="YouTubeジャンル別ランキング", layout="wide")
st.title("📊 ジャンル別 YouTubeチャンネル ランキング（上位30件）")

if not os.path.exists(DATA_FOLDER):
    st.error("データフォルダが見つかりません。")
    st.stop()

ジャンル一覧 = sorted([f.replace(".csv", "") for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")])
if not ジャンル一覧:
    st.error("CSVファイルが見つかりません。")
    st.stop()

ジャンル = st.selectbox("ジャンルを選択", ジャンル一覧)
検索 = st.text_input("🔍 チャンネル名でフィルタ")

# 読み込み
csv_path = os.path.join(DATA_FOLDER, f"{ジャンル}.csv")
df = pd.read_csv(csv_path)

# フィルタ
if 検索:
    df = df[df["チャンネル名"].str.contains(検索, case=False, na=False)]

if df.empty:
    st.warning("該当するチャンネルは見つかりませんでした。")
    st.stop()

# 並び替え（再生数が数値で存在する場合）
if "総再生数" in df.columns:
    try:
        df["再生数_int"] = df["総再生数"].replace({",": ""}, regex=True).astype(int)
        df = df.sort_values(by="再生数_int", ascending=False).reset_index(drop=True)
    except:
        pass

# 表示
for i, row in df.iterrows():
    st.markdown(f"## {row['チャンネル名']}")
    if "URL" in row:
        st.markdown(f"[チャンネルを開く]({row['URL']})")

    if "サムネイルURL" in row:
        st.image(row["サムネイルURL"], width=320)

    チャンネルID = row.get("チャンネルID")
    if チャンネルID:
        history_file = os.path.join(DATA_FOLDER, f"{ジャンル}", f"{チャンネルID}_history.csv")
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
