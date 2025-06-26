import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="ジャンル別YouTubeチャンネルギャラリー")

df = pd.read_csv("data/ranking_output.csv")
with open("data/ranking_with_videos.json", encoding="utf-8") as f:
    video_data = json.load(f)

genre = st.selectbox("ジャンルを選択", sorted(df["ジャンル"].unique()))
search = st.text_input("チャンネル名で検索")

filtered = df[df["ジャンル"] == genre]
if search:
    filtered = filtered[filtered["チャンネル"].str.contains(search, case=False)]

for _, row in filtered.iterrows():
    st.markdown(f"## {row['チャンネル']}（再生数：{row['再生数']:,}）")
    for video in video_data.get(row["チャンネル"], []):
        st.image(f"https://i.ytimg.com/vi/{video['link'].split('=')[-1]}/mqdefault.jpg", width=300)
        st.markdown(f"[{video['title']}]({video['link']}) - {video['published']}")

# グラフ（過去30日）
st.subheader("📈 チャンネル再生数の推移")
history = pd.read_csv("data/ranking_history.csv")
channels = filtered["チャンネル"].tolist()

for channel in channels:
    plot_data = history[history["チャンネル"] == channel].sort_values("日付")
    plt.plot(plot_data["日付"], plot_data["再生数"], label=channel)

plt.xticks(rotation=45)
plt.ylabel("再生数")
plt.legend()
st.pyplot(plt)
