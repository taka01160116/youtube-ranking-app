import datetime
import pandas as pd
from socialblade_scraper import create_ranking

# 1. ランキング取得
df_today = create_ranking()
df_today["日付"] = datetime.date.today().isoformat()

# 2. 履歴ファイルに追記
history_path = "data/ranking_history.csv"
try:
    df_history = pd.read_csv(history_path)
except FileNotFoundError:
    df_history = pd.DataFrame()

df_all = pd.concat([df_history, df_today], ignore_index=True)
df_all.to_csv(history_path, index=False)
