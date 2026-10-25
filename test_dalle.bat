@echo off
cd /d "%~dp0"
set "PY=python"
where py >nul 2>nul && set "PY=py -3"
echo Mire de test pendant 6 secondes (rouge, vert, bleu, cadre).
%PY% arcadedmd.py test
pause
