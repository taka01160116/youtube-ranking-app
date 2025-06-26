@echo off
cd /d C:\Users\PC_User\Desktop\youtube-ranking-app

echo [%DATE% %TIME%] 再生数ランキングのスクレイピング開始...
python scrape_socialblade.py

echo [%DATE% %TIME%] チャンネル再生履歴の更新開始...
python update_history.py

echo [%DATE% %TIME%] 自動更新完了。
pause
