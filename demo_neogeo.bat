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
echo  36  Mutation Nation
echo  37  Sengoku
echo  38  Sengoku 2
echo  39  Ninja Combat
echo  40  Ninja Commando
echo  41  Blue's Journey
echo  42  Puzzle Bobble 2
echo  43  Magical Drop II
echo  44  Money Puzzle Exchanger
echo  45  Puzzle De Pon!
echo  46  Puzzle De Pon! R!
echo  47  Panic Bomber
echo  48  Pop 'n Bounce
echo  49  Super Bubble Pop
echo  50  Spin Master
echo  51  Ganryu
echo  52  Zupapa!
echo  53  Neo Mr. Do!
echo  54  Super Sidekicks
echo  55  Super Sidekicks 2
echo  56  Tecmo World Soccer '96
echo  57  Goal! Goal! Goal!
echo  58  Neo-Geo Cup '98
echo  59  Soccer Brawl
echo  60  Football Frenzy
echo  61  Pleasure Goal
echo  62  Baseball Stars Professional
echo  63  2020 Super Baseball
echo  64  Top Player's Golf
echo  65  Power Spikes II
echo  66  Bang Bead
echo  67  Battle Flip Shot
echo  68  Over Top
echo  69  Stakes Winner
echo  70  Stakes Winner 2
echo  71  Jockey Grand Prix
echo  72  Gururin
echo  73  Ghostlop
echo  74  Pochi and Nyaa
echo  75  Puzzled
echo  76  Zintrick
echo  77  Digger Man
echo  78  The Irritating Maze
echo  79  Andro Dunos
echo  80  Captain Tomaday
echo  81  Choutetsu Brikin'ger
echo  82  Last Hope
echo  83  Bang Bang Busters
echo  84  Crossed Swords
echo  85  Eight Man
echo.
set N=
if "%L%"=="fr" (set /p N=Quel jeu, 1 a 85 ? ) else (set /p N=Which game, 1 to 85? )
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
if "%N%"=="36" set G=mutnat
if "%N%"=="37" set G=sengoku
if "%N%"=="38" set G=sengoku2
if "%N%"=="39" set G=ncombat
if "%N%"=="40" set G=ncommand
if "%N%"=="41" set G=bjourney
if "%N%"=="42" set G=pbobbl2n
if "%N%"=="43" set G=magdrop2
if "%N%"=="44" set G=miexchng
if "%N%"=="45" set G=puzzledp
if "%N%"=="46" set G=puzzldpr
if "%N%"=="47" set G=panicbom
if "%N%"=="48" set G=popbounc
if "%N%"=="49" set G=sbp
if "%N%"=="50" set G=spinmast
if "%N%"=="51" set G=ganryu
if "%N%"=="52" set G=zupapa
if "%N%"=="53" set G=neomrdo
if "%N%"=="54" set G=ssideki
if "%N%"=="55" set G=ssideki2
if "%N%"=="56" set G=twsoc96
if "%N%"=="57" set G=goalx3
if "%N%"=="58" set G=neocup98
if "%N%"=="59" set G=socbrawl
if "%N%"=="60" set G=fbfrenzy
if "%N%"=="61" set G=pgoal
if "%N%"=="62" set G=bstars
if "%N%"=="63" set G=2020bb
if "%N%"=="64" set G=tpgolf
if "%N%"=="65" set G=pspikes2
if "%N%"=="66" set G=bangbead
if "%N%"=="67" set G=flipshot
if "%N%"=="68" set G=overtop
if "%N%"=="69" set G=stakwin
if "%N%"=="70" set G=stakwin2
if "%N%"=="71" set G=jockeygp
if "%N%"=="72" set G=gururin
if "%N%"=="73" set G=ghostlop
if "%N%"=="74" set G=pnyaa
if "%N%"=="75" set G=joyjoy
if "%N%"=="76" set G=zintrckb
if "%N%"=="77" set G=diggerma
if "%N%"=="78" set G=irrmaze
if "%N%"=="79" set G=androdun
if "%N%"=="80" set G=ctomaday
if "%N%"=="81" set G=ironclad
if "%N%"=="82" set G=lasthope
if "%N%"=="83" set G=b2b
if "%N%"=="84" set G=crsword
if "%N%"=="85" set G=eightman
:play
if "%L%"=="fr" (echo Demo %G%, avec des valeurs simulees. Echap ou ferme la fenetre pour quitter.) else (echo %G% demo, with simulated values. Press Esc or close the window to quit.)
%PY% arcadedmd.py demo %G%
if errorlevel 1 pause
