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
echo  11  Top Hunter
echo  12  Baseball Stars 2
echo  13  Last Resort
echo  14  Aero Fighters 2
echo  15  Aero Fighters 3
echo  16  Strikers 1945 Plus
echo  17  Street Hoop
echo  18  Super Dodge Ball
echo  19  Neo Bomberman
echo  20  Twinkle Star Sprites
echo  21  League Bowling
echo  22  Neo Drift Out
echo  23  Riding Hero
echo  24  Thrash Rally
echo  25  Magician Lord
echo  26  NAM-1975
echo  27  Cyber-Lip
echo  28  Ghost Pilots
echo  29  Alpha Mission II
echo  30  Viewpoint
echo  31  Zed Blade
echo  32  Prehistoric Isle 2
echo  33  Shock Troopers 2nd Squad
echo  34  Robo Army
echo  35  Burning Fight
echo.
set N=
if "%L%"=="fr" (set /p N=Quel jeu, 1 a 35 ? ) else (set /p N=Which game, 1 to 35? )
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
if "%N%"=="11" set G=tophuntr
if "%N%"=="12" set G=bstars2
if "%N%"=="13" set G=lresort
if "%N%"=="14" set G=sonicwi2
if "%N%"=="15" set G=sonicwi3
if "%N%"=="16" set G=s1945p
if "%N%"=="17" set G=strhoop
if "%N%"=="18" set G=sdodgeb
if "%N%"=="19" set G=neobombe
if "%N%"=="20" set G=twinspri
if "%N%"=="21" set G=lbowling
if "%N%"=="22" set G=neodrift
if "%N%"=="23" set G=ridhero
if "%N%"=="24" set G=trally
if "%N%"=="25" set G=maglord
if "%N%"=="26" set G=nam1975
if "%N%"=="27" set G=cyberlip
if "%N%"=="28" set G=gpilots
if "%N%"=="29" set G=alpham2
if "%N%"=="30" set G=viewpoin
if "%N%"=="31" set G=zedblade
if "%N%"=="32" set G=preisle2
if "%N%"=="33" set G=shocktr2
if "%N%"=="34" set G=roboarmy
if "%N%"=="35" set G=burningf
:play
if "%L%"=="fr" (echo Demo %G%, avec des valeurs simulees. Echap ou ferme la fenetre pour quitter.) else (echo %G% demo, with simulated values. Press Esc or close the window to quit.)
%PY% arcadedmd.py demo %G%
if errorlevel 1 pause
