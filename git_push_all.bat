@echo off
cd /d C:\Users\PC_User\Desktop\youtube-ranking-app

echo.
echo [Git] �t�@�C����S�Ēǉ���...
git add .

echo.
set /p commit_msg="�R�~�b�g���b�Z�[�W����͂��Ă��������i��Fdaily update�j: "
git commit -m "%commit_msg%"

echo.
echo [Git] �����[�g��push��...
git push origin main

echo.
echo [����] ���ׂ�GitHub�ɔ��f����܂����B
pause
