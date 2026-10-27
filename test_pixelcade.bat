@echo off
cd /d "%~dp0"
call "%~dp0dmd\lang.bat"
call "%~dp0dmd\find_python.bat"
if defined PY goto run
if "%L%"=="fr" (echo Python est introuvable. Lance d'abord install.bat.) else (echo Python was not found. Run install.bat first.)
pause
exit /b 1
:run
if "%L%"=="fr" goto fr
echo Test pattern on the Pixelcade LED.
echo pixelweb is stopped during the test, then started again.
echo At the end, the pattern stays on and the test asks you whether the colors are right.
goto go
:fr
echo Mire de test sur la Pixelcade LED.
echo pixelweb est arrete pendant le test puis relance.
echo A la fin, la mire reste affichee et le test te demande si les couleurs sont bonnes.
:go
%PY% arcadedmd.py test-pixelcade
pause
