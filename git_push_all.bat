@echo off
cd /d %~dp0

REM Git�̏�Ԋm�F
echo [1] Git�X�e�[�^�X�m�F��...
git status

REM ���ׂĂ̕ύX�t�@�C���E�V�K�t�H���_�E�폜���܂߂ăX�e�[�W���O
echo [2] ���ׂẴt�@�C�����X�e�[�W�ɒǉ���...
git add -A

REM �R�~�b�g���b�Z�[�W�̓��͂𑣂�
set /p msg=[3] �R�~�b�g���b�Z�[�W����͂��Ă��������i��Fdaily update�j:

if "%msg%"=="" (
    set msg=update all data
)

REM �R�~�b�g�����s
echo [4] �R�~�b�g���s��...
git commit -m "%msg%"

REM GitHub��push
echo [5] GitHub��push��...
git push origin main

echo �������܂����B�E�B���h�E����Ă��������B
pause
