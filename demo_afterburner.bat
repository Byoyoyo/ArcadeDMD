@echo off
cd /d "%~dp0"
set "PY=python"
where py >nul 2>nul && set "PY=py -3"
echo Demo After Burner II (valeurs simulees). Echap ou fermer la fenetre pour quitter.
%PY% arcadedmd.py demo aburner2
if errorlevel 1 pause
