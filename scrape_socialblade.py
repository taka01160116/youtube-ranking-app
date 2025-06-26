# 必要ライブラリをインストールしてください：
# pip install selenium pandas webdriver-manager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

# ====== 設定 ======
ジャンルリスト = {
    "チャレンジ･やってみた": "https://socialblade.com/youtube/top/country/jp/entertainment",
    "レビュー･紹介･解説": "https://socialblade.com/youtube/top/country/jp/people",
    "ゲーム･実況": "https://socialblade.com/youtube/top/country/jp/gaming",
    "Vtuber": "https://socialblade.com/youtube/top/country/jp/vtuber",
    "LIVE･ラジオ": "https://socialblade.com/youtube/top/country/jp/live",
    "企業･会社": "https://socialblade.com/youtube/top/country/jp/news",
    "ビジネス･教養": "https://socialblade.com/youtube/top/country/jp/education",
    "ベビー･子供･キッズ･教育": "https://socialblade.com/youtube/top/country/jp/kids",
    "Web･IT･テクノロジー": "https://socialblade.com/youtube/top/country/jp/science",
    "デザイン･ものづくり": "https://socialblade.com/youtube/top/country/jp/howto",
    "暮らし･雑貨･インテリア": "https://socialblade.com/youtube/top/country/jp/howto",
    "Vlog･日常": "https://socialblade.com/youtube/top/country/jp/people",
    "音楽･ミュージック": "https://socialblade.com/youtube/top/country/jp/music",
    "漫画･アニメ･本": "https://socialblade.com/youtube/top/country/jp/film",
    "美容･ファッション": "https://socialblade.com/youtube/top/country/jp/howto",
    "エンタメ･バラエティ": "https://socialblade.com/youtube/top/country/jp/entertainment",
    "映画･テレビ･芸能": "https://socialblade.com/youtube/top/country/jp/film",
    "料理･グルメ": "https://socialblade.com/youtube/top/country/jp/howto",
    "植物･ペット･生物": "https://socialblade.com/youtube/top/country/jp/pets",
    "カルチャー･芸術": "https://socialblade.com/youtube/top/country/jp/entertainment",
    "スポーツ･健康･運動": "https://socialblade.com/youtube/top/country/jp/sports",
    "病院･医療": "https://socialblade.com/youtube/top/country/jp/education",
    "科学･研究": "https://socialblade.com/youtube/top/country/jp/science",
    "旅行･観光": "https://socialblade.com/youtube/top/country/jp/people",
    "農業･自然": "https://socialblade.com/youtube/top/country/jp/people",
    "車･バイク･乗り物": "https://socialblade.com/youtube/top/country/jp/vehicles",
    "不動産･建築": "https://socialblade.com/youtube/top/country/jp/howto",
    "金融･法律･保険": "https://socialblade.com/youtube/top/country/jp/education",
    "冠婚葬祭": "https://socialblade.com/youtube/top/country/jp/people",
    "介護･お年寄り": "https://socialblade.com/youtube/top/country/jp/people"
}

出力フォルダ = "scraped_channels"
os.makedirs(出力フォルダ, exist_ok=True)

# Chrome起動オプション
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for ジャンル, url in ジャンルリスト.items():
    print(f"取得中: {ジャンル}...")
    driver.get(url)
    time.sleep(5)  # ページ読み込み待ち

    rows = driver.find_elements(By.CSS_SELECTOR, ".table.table-bordered.table-hover tbody tr")

    チャンネルデータ = []
    for row in rows[:30]:  # 上位30件に制限
        try:
            name = row.find_element(By.CSS_SELECTOR, "a").text
            channel_url = row.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            stats = row.find_elements(By.CSS_SELECTOR, "td")
            subs = stats[2].text if len(stats) > 2 else ""
            views = stats[3].text if len(stats) > 3 else ""
            チャンネルデータ.append([name, subs, views, channel_url])
        except Exception as e:
            print("スキップ: エラー", e)
            continue

    df = pd.DataFrame(チャンネルデータ, columns=["チャンネル名", "登録者数", "総再生数", "URL"])
    df.to_csv(os.path.join(出力フォルダ, f"{ジャンル}.csv"), index=False, encoding="utf-8-sig")
    print(f"✅ {ジャンル}：保存完了")

print("✅ すべてのジャンル取得完了")
driver.quit()
