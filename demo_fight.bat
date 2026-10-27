@echo off
cd /d "%~dp0"
call "%~dp0dmd\lang.bat"
call "%~dp0dmd\find_python.bat"
if defined PY goto run
if "%L%"=="fr" (echo Python est introuvable. Lance d'abord install.bat.) else (echo Python was not found. Run install.bat first.)
pause
exit /b 1
:run
if "%L%"=="fr" (echo Demo jeu de combat, The King of Fighters '98, avec des valeurs simulees. Echap ou ferme la fenetre pour quitter.) else (echo Fighting game demo, The King of Fighters '98, with simulated values. Press Esc or close the window to quit.)
%PY% arcadedmd.py demo kof98
if errorlevel 1 pause
