@echo off
cd /d "%~dp0"
set "PY=python"
where py >nul 2>nul && set "PY=py -3"
echo Mire de test sur la Pixelcade LED.
echo pixelweb est arrete pendant le test puis relance.
echo A la fin, la mire reste affichee et le test te demande si les couleurs sont bonnes.
%PY% arcadedmd.py test-pixelcade
pause
