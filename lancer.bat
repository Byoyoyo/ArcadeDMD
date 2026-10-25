@echo off
cd /d "%~dp0"
set "PY=python"
where py >nul 2>nul && set "PY=py -3"
echo ArcadeDMD tourne. Ferme cette fenetre pour l'arreter.
%PY% arcadedmd.py
pause
