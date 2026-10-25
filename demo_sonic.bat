@echo off
cd /d "%~dp0"
set "PY=python"
where py >nul 2>nul && set "PY=py -3"
echo Demo Sonic (valeurs simulees). Echap ou fermer la fenetre pour quitter.
%PY% arcadedmd.py demo sonic
if errorlevel 1 pause
