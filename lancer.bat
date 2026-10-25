@echo off
cd /d "%~dp0"
call "%~dp0dmd\trouver_python.bat"
if not defined PY (
  echo Python est introuvable. Lance d'abord installer.bat.
  pause
  exit /b 1
)
echo ArcadeDMD tourne. Ferme cette fenetre pour l'arreter.
%PY% arcadedmd.py
pause
