@echo off
cd /d "%~dp0"
call "%~dp0dmd\trouver_python.bat"
if not defined PY (
  echo Python est introuvable. Lance d'abord installer.bat.
  pause
  exit /b 1
)
echo Mire de test sur la Pixelcade LED.
echo pixelweb est arrete pendant le test puis relance.
echo A la fin, la mire reste affichee et le test te demande si les couleurs sont bonnes.
%PY% arcadedmd.py test-pixelcade
pause
