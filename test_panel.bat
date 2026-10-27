@echo off
cd /d "%~dp0"
call "%~dp0dmd\lang.bat"
call "%~dp0dmd\find_python.bat"
if defined PY goto run
if "%L%"=="fr" (echo Python est introuvable. Lance d'abord install.bat.) else (echo Python was not found. Run install.bat first.)
pause
exit /b 1
:run
if "%L%"=="fr" (echo Mire de test pendant 6 secondes, rouge, vert, bleu puis cadre.) else (echo Test pattern for 6 seconds, red, green, blue, then a frame.)
%PY% arcadedmd.py test
pause
