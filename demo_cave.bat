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
echo   1  Air Gallet
echo   2  Akai Katana
echo   3  Bishoujo Senshi Sailor Moon
echo   4  Crusher Makochan
echo   5  Deathsmiles
echo   6  Deathsmiles MegaBlack Label
echo   7  DoDonPachi
echo   8  DoDonPachi Dai-Fukkatsu Black Label
echo   9  DoDonPachi Dai-Fukkatsu Ver 1.5
echo  10  DoDonPachi Dai-Ou-Jou
echo  11  DoDonPachi II - Bee Storm
echo  12  DoDonPachi SaiDaiOuJou
echo  13  DonPachi
echo  14  ESP Ra.De. - A.D.2018 Tokyo
echo  15  Espgaluda
echo  16  Espgaluda II
echo  17  Fever SOS
echo  18  Gaia Crusaders
echo  19  Gogetsuji Legends
echo  20  Guwange
echo  21  Hotdog Storm - The First Supersonics
echo  22  Ibara
echo  23  Ibara Kuro Black Label
echo  24  Ketsui: Kizuna Jigoku Tachi
echo  25  Koro Koro Quest
echo  26  Mazinger Z
echo  27  Metamoqester
echo  28  Muchi Muchi Pork^!
echo  29  Mushihime-Sama
echo  30  Mushihime-Sama Futari Black Label - Another Ver
echo  31  Mushihime-Sama Futari Ver 1.5
echo  32  Mushihime-Sama Matsuri Ver 1.5
echo  33  Pink Sweets: Ibara Sorekara
echo  34  Power Instinct 2
echo  35  Puzzle Uo Poko
echo  36  Puzzle^! Mushihime-Tama
echo  37  Thunder Heroes
echo.
set N=
if "%L%"=="fr" (set /p N=Quel jeu, 1 a 37 ? ) else (set /p N=Which game, 1 to 37? )
set G=agallet
if "%N%"=="2" set G=akatana
if "%N%"=="3" set G=sailormn
if "%N%"=="4" set G=crusherm
if "%N%"=="5" set G=deathsml
if "%N%"=="6" set G=dsmbl
if "%N%"=="7" set G=ddonpach
if "%N%"=="8" set G=dfkbl
if "%N%"=="9" set G=ddpdfk
if "%N%"=="10" set G=ddp3
if "%N%"=="11" set G=ddp2
if "%N%"=="12" set G=ddpsdoj
if "%N%"=="13" set G=donpachi
if "%N%"=="14" set G=esprade
if "%N%"=="15" set G=espgal
if "%N%"=="16" set G=espgal2
if "%N%"=="17" set G=feversos
if "%N%"=="18" set G=gaia
if "%N%"=="19" set G=plegends
if "%N%"=="20" set G=guwange
if "%N%"=="21" set G=hotdogst
if "%N%"=="22" set G=ibara
if "%N%"=="23" set G=ibarablk
if "%N%"=="24" set G=ket
if "%N%"=="25" set G=korokoro
if "%N%"=="26" set G=mazinger
if "%N%"=="27" set G=metmqstr
if "%N%"=="28" set G=mmpork
if "%N%"=="29" set G=mushisam
if "%N%"=="30" set G=futaribl
if "%N%"=="31" set G=futari15
if "%N%"=="32" set G=matsuri15
if "%N%"=="33" set G=pinkswts
if "%N%"=="34" set G=pwrinst2
if "%N%"=="35" set G=uopoko
if "%N%"=="36" set G=mushitam
if "%N%"=="37" set G=theroes
:play
if "%L%"=="fr" (echo Demo %G%, avec des valeurs simulees. Echap ou ferme la fenetre pour quitter.) else (echo %G% demo, with simulated values. Press Esc or close the window to quit.)
%PY% arcadedmd.py demo %G%
if errorlevel 1 pause
