@echo off
cd /d "%~dp0"
set "PY=python"
where py >nul 2>nul && set "PY=py -3"
echo Mire de test sur la Pixelcade LED pendant 6 secondes.
echo pixelweb est arrete pendant le test puis relance.
%PY% arcadedmd.py test-pixelcade
pause
