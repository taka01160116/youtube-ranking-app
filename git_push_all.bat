@echo off
cd /d %~dp0

REM Gitの状態確認
echo [1] Gitステータス確認中...
git status

REM すべての変更ファイル・新規フォルダ・削除も含めてステージング
echo [2] すべてのファイルをステージに追加中...
git add -A

REM コミットメッセージの入力を促す
set /p msg=[3] コミットメッセージを入力してください（例：daily update）:

if "%msg%"=="" (
    set msg=update all data
)

REM コミットを実行
echo [4] コミット実行中...
git commit -m "%msg%"

REM GitHubへpush
echo [5] GitHubにpush中...
git push origin main

echo 完了しました。ウィンドウを閉じてください。
pause
