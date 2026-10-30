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
echo   1  1941: Counter Attack
echo   2  1944: The Loop Master
echo   3  19XX: The War Against Destiny
echo   4  Adventure Quiz Capcom World 2
echo   5  Alien vs. Predator
echo   6  Armored Warriors
echo   7  Battle Circuit
echo   8  Cadillacs and Dinosaurs
echo   9  Capcom Sports Club
echo  10  Captain Commando
echo  11  Carrier Air Wing
echo  12  Cyberbots: Fullmetal Madness
echo  13  Darkstalkers: The Night Warriors
echo  14  Dimahoo
echo  15  Dungeons ^& Dragons: Shadow over Mystara
echo  16  Dungeons ^& Dragons: Tower of Doom
echo  17  Dynasty Wars
echo  18  Eco Fighters
echo  19  Final Fight
echo  20  Final Fight EX
echo  21  Final Fight: Anniversary Edition
echo  22  Forgotten Worlds
echo  23  Frog Feast
echo  24  Ganbare! Marine Kun
echo  25  Ghouls'n Ghosts
echo  26  Giga Wing
echo  27  Gulun.Pa!
echo  28  Hyper Street Fighter II: The Anniversary Edition
echo  29  Janpai Puzzle Choukou
echo  30  JoJo's Bizarre Adventure
echo  31  JoJo's Venture
echo  32  Jyangokushi: Haoh no Saihai
echo  33  The King of Dragons
echo  34  Knights of the Round
echo  35  Magic Sword: Heroic Fantasy
echo  36  Magical Pumpkin: Puroland de Daibouken
echo  37  Mars Matrix: Hyper Solid Shooting
echo  38  Marvel Super Heroes
echo  39  Marvel Super Heroes Vs. Street Fighter
echo  40  Marvel Vs. Capcom: Clash of Super Heroes
echo  41  Mega Man 2: The Power Fighters
echo  42  Mega Man: The Power Battle
echo  43  Mega Twins
echo  44  Mercs
echo  45  Mighty! Pang
echo  46  Muscle Bomber Duo: Ultimate Team Battle
echo  47  Nemo
echo  48  Night Warriors: Darkstalkers' Revenge
echo  49  Pang! 3
echo  50  Pnickies
echo  51  Pokonyan! Balloon
echo  52  Progear
echo  53  The Punisher
echo  54  Puzz Loop 2
echo  55  Quiz ^& Dragons: Capcom Quiz Game
echo  56  Quiz Nanairo Dreams: Nijiirochou no Kiseki
echo  57  Quiz Tonosama no Yabou 2: Zenkoku-ban
echo  58  Red Earth
echo  59  Ring of Destruction: Slammasters II
echo  60  Saturday Night Slam Masters
echo  61  Street Fighter Alpha 2
echo  62  Street Fighter Alpha 3
echo  63  Street Fighter Alpha: Warriors' Dreams
echo  64  Street Fighter II': Champion Edition
echo  65  Street Fighter II': Hyper Fighting
echo  66  Street Fighter II: The World Warrior
echo  67  Street Fighter III 2nd Impact: Giant Attack
echo  68  Street Fighter III 3rd Strike: Fight for the Future
echo  69  Street Fighter III: New Generation
echo  70  Street Fighter Zero
echo  71  Street Fighter Zero 2 Alpha
echo  72  Strider
echo  73  Super Gem Fighter: Mini Mix
echo  74  Super Puzzle Fighter II Turbo
echo  75  Super Street Fighter II Turbo
echo  76  Super Street Fighter II: The New Challengers
echo  77  Tenchi wo Kurau II: Sekiheki no Tatakai
echo  78  Three Wonders
echo  79  U.N. Squadron
echo  80  Vampire Hunter 2: Darkstalkers Revenge
echo  81  Vampire Savior 2: The Lord of Vampire
echo  82  Vampire Savior: The Lord of Vampire
echo  83  Varth: Operation Thunderstorm
echo  84  Warriors of Fate
echo  85  Willow
echo  86  X-Men Vs. Street Fighter
echo  87  X-Men: Children of the Atom
echo.
set N=
if "%L%"=="fr" (set /p N=Quel jeu, 1 a 87 ? ) else (set /p N=Which game, 1 to 87? )
set G=1941
if "%N%"=="2" set G=1944
if "%N%"=="3" set G=19xx
if "%N%"=="4" set G=cworld2j
if "%N%"=="5" set G=avsp
if "%N%"=="6" set G=armwar
if "%N%"=="7" set G=batcir
if "%N%"=="8" set G=dino
if "%N%"=="9" set G=csclub
if "%N%"=="10" set G=captcomm
if "%N%"=="11" set G=cawing
if "%N%"=="12" set G=cybots
if "%N%"=="13" set G=dstlk
if "%N%"=="14" set G=dimahoo
if "%N%"=="15" set G=ddsom
if "%N%"=="16" set G=ddtod
if "%N%"=="17" set G=dynwar
if "%N%"=="18" set G=ecofghtr
if "%N%"=="19" set G=ffight
if "%N%"=="20" set G=ffex2u
if "%N%"=="21" set G=ffightaec2
if "%N%"=="22" set G=forgottn
if "%N%"=="23" set G=cps1frog
if "%N%"=="24" set G=ganbare
if "%N%"=="25" set G=ghouls
if "%N%"=="26" set G=gigawing
if "%N%"=="27" set G=gulunpa
if "%N%"=="28" set G=hsf2
if "%N%"=="29" set G=choko
if "%N%"=="30" set G=jojoba
if "%N%"=="31" set G=jojo
if "%N%"=="32" set G=jyangoku
if "%N%"=="33" set G=kod
if "%N%"=="34" set G=knights
if "%N%"=="35" set G=msword
if "%N%"=="36" set G=mpumpkin
if "%N%"=="37" set G=mmatrix
if "%N%"=="38" set G=msh
if "%N%"=="39" set G=mshvsf
if "%N%"=="40" set G=mvsc
if "%N%"=="41" set G=megaman2
if "%N%"=="42" set G=megaman
if "%N%"=="43" set G=mtwins
if "%N%"=="44" set G=mercs
if "%N%"=="45" set G=mpang
if "%N%"=="46" set G=mbombrd
if "%N%"=="47" set G=nemo
if "%N%"=="48" set G=nwarr
if "%N%"=="49" set G=pang3
if "%N%"=="50" set G=pnickj
if "%N%"=="51" set G=pokonyan
if "%N%"=="52" set G=progear
if "%N%"=="53" set G=punisher
if "%N%"=="54" set G=pzloop2
if "%N%"=="55" set G=qad
if "%N%"=="56" set G=qndream
if "%N%"=="57" set G=qtono2j
if "%N%"=="58" set G=redearth
if "%N%"=="59" set G=ringdest
if "%N%"=="60" set G=slammast
if "%N%"=="61" set G=sfa2
if "%N%"=="62" set G=sfa3
if "%N%"=="63" set G=sfa
if "%N%"=="64" set G=sf2ce
if "%N%"=="65" set G=sf2hf
if "%N%"=="66" set G=sf2
if "%N%"=="67" set G=sfiii2
if "%N%"=="68" set G=sfiii3
if "%N%"=="69" set G=sfiii
if "%N%"=="70" set G=sfzch
if "%N%"=="71" set G=sfz2al
if "%N%"=="72" set G=strider
if "%N%"=="73" set G=sgemf
if "%N%"=="74" set G=spf2t
if "%N%"=="75" set G=ssf2t
if "%N%"=="76" set G=ssf2
if "%N%"=="77" set G=wofch
if "%N%"=="78" set G=3wonders
if "%N%"=="79" set G=unsquad
if "%N%"=="80" set G=vhunt2
if "%N%"=="81" set G=vsav2
if "%N%"=="82" set G=vsav
if "%N%"=="83" set G=varth
if "%N%"=="84" set G=wof
if "%N%"=="85" set G=willow
if "%N%"=="86" set G=xmvsf
if "%N%"=="87" set G=xmcota
:play
if "%L%"=="fr" (echo Demo %G%, avec des valeurs simulees. Echap ou ferme la fenetre pour quitter.) else (echo %G% demo, with simulated values. Press Esc or close the window to quit.)
%PY% arcadedmd.py demo %G%
if errorlevel 1 pause
