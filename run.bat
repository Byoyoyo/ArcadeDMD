@echo off
rem Starts ArcadeDMD without a console: its icon sits near the clock and its window opens.
rem run_console.bat starts it with a console, to look for a problem.
rem Lance ArcadeDMD sans console : son icone se met pres de l'horloge et sa fenetre s'ouvre.
rem run_console.bat le lance avec une console, pour chercher un probleme.
cd /d "%~dp0"
call "%~dp0dmd\lang.bat"
call "%~dp0dmd\find_python.bat"
if defined PY goto run
if "%L%"=="fr" (echo Python est introuvable. Lance d'abord install.bat.) else (echo Python was not found. Run install.bat first.)
pause
exit /b 1
:run
if not defined PYW set "PYW=%PY%"
start "" %PYW% arcadedmd.py --window
if "%L%"=="fr" (echo ArcadeDMD tourne pres de l'horloge et sa fenetre s'ouvre.) else (echo ArcadeDMD runs near the clock and its window opens.)
timeout /t 3 >nul
