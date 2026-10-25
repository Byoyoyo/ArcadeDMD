@echo off
cd /d "%~dp0"
call "%~dp0dmd\trouver_python.bat"
if not defined PY (
  echo Python est introuvable. Lance d'abord installer.bat.
  pause
  exit /b 1
)
echo Mire de test pendant 6 secondes (rouge, vert, bleu, cadre).
%PY% arcadedmd.py test
pause
