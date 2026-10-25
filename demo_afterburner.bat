@echo off
cd /d "%~dp0"
call "%~dp0dmd\trouver_python.bat"
if not defined PY (
  echo Python est introuvable. Lance d'abord installer.bat.
  pause
  exit /b 1
)
echo Demo After Burner II (valeurs simulees). Echap ou fermer la fenetre pour quitter.
%PY% arcadedmd.py demo aburner2
if errorlevel 1 pause
