@echo off
rem ArcadeDMD with its console, as before 1.37, to look for a problem.
rem ArcadeDMD avec sa console, comme avant la 1.37, pour chercher un probleme.
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
