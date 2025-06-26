@echo off
cd /d C:\Users\PC_User\Desktop\youtube-ranking-app

echo.
echo [Git] ファイルを全て追加中...
git add .

echo.
set /p commit_msg="コミットメッセージを入力してください（例：daily update）: "
git commit -m "%commit_msg%"

echo.
echo [Git] リモートにpush中...
git push origin main

echo.
echo [完了] すべてGitHubに反映されました。
pause
