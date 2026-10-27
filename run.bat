@echo off
cd /d "%~dp0"
call "%~dp0dmd\lang.bat"
call "%~dp0dmd\find_python.bat"
if defined PY goto run
if "%L%"=="fr" (echo Python est introuvable. Lance d'abord install.bat.) else (echo Python was not found. Run install.bat first.)
pause
exit /b 1
:run
if "%L%"=="fr" (echo ArcadeDMD tourne. Ferme cette fenetre pour l'arreter.) else (echo ArcadeDMD is running. Close this window to stop it.)
%PY% arcadedmd.py
pause
