@echo off
cd /d "%~dp0"
call "%~dp0dmd\lang.bat"
call "%~dp0dmd\find_python.bat"
if defined PY goto run
if "%L%"=="fr" (echo Python est introuvable. Lance d'abord install.bat.) else (echo Python was not found. Run install.bat first.)
pause
exit /b 1
:run
set G=%~1
if not "%G%"=="" goto play
echo.
echo   1  Blazing Star
echo   2  Puzzle Bobble
echo   3  Windjammers
echo   4  Shock Troopers
echo   5  Neo Turf Masters
echo   6  Pulstar
echo   7  Magical Drop III
echo   8  Super Sidekicks 3
echo   9  The Ultimate 11
echo  10  Sengoku 3
echo.
set N=
if "%L%"=="fr" (set /p N=Quel jeu, 1 a 10 ? ) else (set /p N=Which game, 1 to 10? )
set G=blazstar
if "%N%"=="2" set G=pbobblen
if "%N%"=="3" set G=wjammers
if "%N%"=="4" set G=shocktro
if "%N%"=="5" set G=turfmast
if "%N%"=="6" set G=pulstar
if "%N%"=="7" set G=magdrop3
if "%N%"=="8" set G=ssideki3
if "%N%"=="9" set G=ssideki4
if "%N%"=="10" set G=sengoku3
:play
if "%L%"=="fr" (echo Demo %G%, avec des valeurs simulees. Echap ou ferme la fenetre pour quitter.) else (echo %G% demo, with simulated values. Press Esc or close the window to quit.)
%PY% arcadedmd.py demo %G%
if errorlevel 1 pause
