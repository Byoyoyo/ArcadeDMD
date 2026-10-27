@echo off
rem ArcadeDMD setup. Messages in English, or in French when Windows (or config.json) is in French.
rem Installation d'ArcadeDMD. Messages en anglais, ou en francais quand Windows (ou config.json) est en francais.
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"
if not exist config.json if exist config.default.json copy /y config.default.json config.json >nul
call "%~dp0dmd\lang.bat"
set "ARCADEDMD_LANG=%L%"
call :messages
echo ==============================================
echo !%L%_TITLE!
echo ==============================================
echo.

rem ---------- Files of older versions, renamed in English since 1.15 ----------
set "OLD="
for %%F in (lancer.bat apprendre.bat installer.bat ecran_dmd.bat test_dalle.bat demo_combat.bat dmd\trouver_python.bat config.defaut.json LISEZMOI.md sprites\LISEZMOI.txt libzedmd\LISEZMOI.txt) do (
  if exist "%%F" (
    del /q "%%F" >nul 2>nul
    set "OLD=1"
  )
)
if defined OLD (
  echo !%L%_OLD1!
  echo !%L%_OLD2!
  echo.
)

rem ---------- 1. Python and libraries ----------
call "%~dp0dmd\find_python.bat"
if defined PY goto python_ok
echo !%L%_NOPY1!
echo !%L%_NOPY2!
where winget >nul 2>nul
if errorlevel 1 goto python_manual
set "ANS="
set /p "ANS=  !%L%_Q_PY! "
call :yesno
if "!ANS!"=="n" goto python_manual
winget install -e --id Python.Python.3.13 --scope user --accept-package-agreements --accept-source-agreements
call "%~dp0dmd\find_python.bat"
if defined PY goto python_ok
:python_manual
echo !%L%_PYMAN1!
echo !%L%_PYMAN2!
pause
exit /b 1
:python_ok
echo [1/6] !%L%_S1!
echo   !%L%_PYUSED! !PY!
%PY% -m pip install --upgrade pillow pyserial
if errorlevel 1 (
  echo !%L%_PIPFAIL!
  pause
  exit /b 1
)
%PY% -c "import pygame" >nul 2>nul
if errorlevel 1 (
  %PY% -m pip install --upgrade pygame-ce
  if errorlevel 1 echo   !%L%_NOPYGAME!
) else (
  echo   !%L%_PYGAMEOK!
)

rem ---------- 2. ZeDMD (optional) ----------
echo.
echo [2/6] !%L%_S2!
echo   !%L%_Z_ONLY!
set "ANS="
set /p "ANS=  !%L%_Q_Z! "
call :yesno
if not "!ANS!"=="y" (
  echo   !%L%_Z_SKIP!
  goto zedmd_done
)
%PY% arcadedmd.py check-zedmd >nul 2>nul
if errorlevel 1 (
  set "ZVER=0.11.0"
  set "ZURL=https://github.com/PPUC/libzedmd/releases/download/v!ZVER!/libzedmd-!ZVER!-win-mingw-x64-Release.zip"
  echo   !%L%_Z_DL! !ZURL!
  curl -L -f -s -o "%TEMP%\libzedmd.zip" "!ZURL!"
  if errorlevel 1 (
    echo   !%L%_Z_DLFAIL!
  ) else (
    if not exist libzedmd mkdir libzedmd
    tar -xf "%TEMP%\libzedmd.zip" -C libzedmd
  )
)
%PY% arcadedmd.py check-zedmd
if errorlevel 1 (
  echo   !%L%_Z_MAN1!
  echo   !%L%_Z_MAN2!
)
%PY% arcadedmd.py enable-zedmd
:zedmd_done

rem ---------- 3. MAME plugin ----------
echo.
echo [3/6] !%L%_S3!
set "MAMEDIR="
for %%D in ("%USERPROFILE%\LaunchBox\Emulators\MAME" "C:\LaunchBox\Emulators\MAME" "D:\LaunchBox\Emulators\MAME" "E:\LaunchBox\Emulators\MAME" "C:\HyperSpin\Emulators\MAME" "D:\HyperSpin\Emulators\MAME" "E:\HyperSpin\Emulators\MAME" "C:\Emulateurs\MAME" "D:\Emulateurs\MAME" "C:\Emulators\MAME" "D:\Emulators\MAME" "C:\MAME" "D:\MAME" "E:\MAME") do (
  if not defined MAMEDIR if exist "%%~D\mame.exe" set "MAMEDIR=%%~D"
  if not defined MAMEDIR if exist "%%~D\mame64.exe" set "MAMEDIR=%%~D"
  if not defined MAMEDIR if exist "%%~D\plugins\boot.lua" set "MAMEDIR=%%~D"
)
set /a TRIES=0
:ask_mame
set /a TRIES+=1
if !TRIES! GTR 5 goto skip_mame
set "ANS="
if defined MAMEDIR echo   !%L%_M_FOUND! !MAMEDIR!
if defined MAMEDIR echo   !%L%_M_KEEP!
if not defined MAMEDIR echo   !%L%_M_NONE!
set /p "ANS=  !%L%_Q_M! "
if defined ANS set "ANS=!ANS:"=!"
if defined ANS set "MAMEDIR=!ANS!"
if not defined MAMEDIR goto skip_mame
%PY% arcadedmd.py install-plugin "!MAMEDIR!"
if errorlevel 2 (
  pause
  exit /b 1
)
if errorlevel 1 (
  set "MAMEDIR="
  echo   !%L%_M_AGAIN!
  goto ask_mame
)
goto mame_done
:skip_mame
echo   !%L%_M_SKIP!
:mame_done

rem ---------- 4. Pixelcade ----------
echo.
echo [4/6] Pixelcade LED
set "ANS="
set /p "ANS=  !%L%_Q_PC! "
call :yesno
if "!ANS!"=="y" %PY% arcadedmd.py setup-pixelcade

rem ---------- 5. LCD screen used as a DMD ----------
echo.
echo [5/6] !%L%_S5!
set "ANS="
set /p "ANS=  !%L%_Q_LCD! "
call :yesno
if "!ANS!"=="y" %PY% arcadedmd.py setup-screen

rem ---------- 6. Start with Windows ----------
echo.
echo [6/6] !%L%_S6!
set "ANS="
set /p "ANS=  !%L%_Q_AUTO! "
call :yesno
if "!ANS!"=="n" goto done
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
> "!STARTUP!\ArcadeDMD.bat" echo @echo off
>> "!STARTUP!\ArcadeDMD.bat" echo cd /d "!ROOT!"
>> "!STARTUP!\ArcadeDMD.bat" echo start "" !PYW! "!ROOT!\arcadedmd.py"
echo   !%L%_AUTO_OK!

:done
echo.
echo !%L%_DONE!
echo !%L%_T1!
echo !%L%_T2!
echo !%L%_T3!
echo !%L%_T4!
echo !%L%_T5!
echo.
pause
exit /b 0

rem ---------- Answers: y, yes, o, oui = y ; n, no, non = n ----------
:yesno
if not defined ANS exit /b 0
set "ANS=%ANS:"=%"
if not defined ANS exit /b 0
set "ANS=%ANS:~0,1%"
if /i "%ANS%"=="o" set "ANS=y"
if /i "%ANS%"=="y" set "ANS=y"
if /i "%ANS%"=="n" set "ANS=n"
exit /b 0

rem ---------- Messages (en_ English, fr_ French, no accents for the console) ----------
:messages
set "en_TITLE=  ArcadeDMD setup"
set "fr_TITLE=  Installation ArcadeDMD"
set "en_OLD1=The launchers of older versions had French names. They were removed."
set "fr_OLD1=Les .bat des anciennes versions avaient des noms francais. Ils ont ete supprimes."
set "en_OLD2=From now on, use run.bat, learn.bat, screen_setup.bat and test_panel.bat."
set "fr_OLD2=Utilise maintenant run.bat, learn.bat, screen_setup.bat et test_panel.bat."
set "en_NOPY1=Python is not installed on this PC."
set "fr_NOPY1=Python n'est pas installe sur ce PC."
set "en_NOPY2=The Microsoft Store "python" shortcut does not count, it does not run anything."
set "fr_NOPY2=Le raccourci "python" du Microsoft Store ne compte pas, il ne lance rien."
set "en_Q_PY=Install Python 3.13 now from python.org? (Y/n):"
set "fr_Q_PY=Installer Python 3.13 maintenant depuis python.org ? (O/n) :"
set "en_PYMAN1=Install Python 3.13 from https://www.python.org/downloads/ and tick "Add python.exe to PATH","
set "fr_PYMAN1=Installe Python 3.13 depuis https://www.python.org/downloads/ en cochant "Add python.exe to PATH","
set "en_PYMAN2=then run install.bat again."
set "fr_PYMAN2=puis relance install.bat."
set "en_S1=Python libraries"
set "fr_S1=Bibliotheques Python"
set "en_PYUSED=Python used"
set "fr_PYUSED=Python utilise"
set "en_PIPFAIL=Pillow or pyserial could not be installed. Check the internet connection, then run install.bat again."
set "fr_PIPFAIL=Echec de l'installation de Pillow ou pyserial. Verifie la connexion internet puis relance install.bat."
set "en_NOPYGAME=pygame-ce not installed. The virtual LED window will use tkinter, which is slower."
set "fr_NOPYGAME=pygame-ce non installe. La fenetre LED virtuelles utilisera tkinter, plus lente."
set "en_PYGAMEOK=pygame already installed."
set "fr_PYGAMEOK=pygame deja present."
set "en_S2=ZeDMD panel"
set "fr_S2=Dalle ZeDMD"
set "en_Z_ONLY=Only if you also have a ZeDMD panel. With a Pixelcade only, just press Enter."
set "fr_Z_ONLY=Seulement si tu as une dalle ZeDMD en plus. Avec une Pixelcade seule, appuie sur Entree."
set "en_Q_Z=Do you have a ZeDMD panel? (y/N):"
set "fr_Q_Z=As-tu une dalle ZeDMD ? (o/N) :"
set "en_Z_SKIP=No ZeDMD, step skipped."
set "fr_Z_SKIP=Pas de ZeDMD, etape ignoree."
set "en_Z_DL=Downloading"
set "fr_Z_DL=Telechargement de"
set "en_Z_DLFAIL=Download failed."
set "fr_Z_DLFAIL=Telechargement impossible."
set "en_Z_MAN1=Download the "win-mingw-x64-Release" archive by hand from https://github.com/PPUC/libzedmd/releases"
set "fr_Z_MAN1=Recupere a la main l'archive "win-mingw-x64-Release" sur https://github.com/PPUC/libzedmd/releases"
set "en_Z_MAN2=and copy all its DLL files into the libzedmd folder of ArcadeDMD."
set "fr_Z_MAN2=et copie toutes ses DLL dans le dossier libzedmd d'ArcadeDMD."
set "en_S3=MAME plugin"
set "fr_S3=Plugin MAME"
set "en_M_FOUND=MAME found in"
set "fr_M_FOUND=MAME trouve dans"
set "en_M_KEEP=Press Enter to keep it."
set "fr_M_KEEP=Appuie sur Entree pour le garder."
set "en_M_NONE=If you do not use MAME (RetroArch only), just press Enter."
set "fr_M_NONE=Si tu n'utilises pas MAME (seulement RetroArch), appuie simplement sur Entree."
set "en_Q_M=MAME folder, the one that contains mame.exe:"
set "fr_Q_M=Dossier de MAME, celui qui contient mame.exe :"
set "en_M_AGAIN=Enter the right folder, or press Enter to skip."
set "fr_M_AGAIN=Indique le bon dossier, ou appuie sur Entree pour passer."
set "en_M_SKIP=MAME plugin not installed. Run install.bat again the day you want to use it with MAME."
set "fr_M_SKIP=Plugin MAME non installe. Relance install.bat le jour ou tu veux l'utiliser avec MAME."
set "en_Q_PC=Do you have a Pixelcade LED to drive? (y/N):"
set "fr_Q_PC=As-tu une Pixelcade LED a piloter ? (o/N) :"
set "en_S5=LCD screen used as a DMD"
set "fr_S5=Ecran LCD qui sert de DMD"
set "en_Q_LCD=Do you have an extra LCD screen used as a DMD? (y/N):"
set "fr_Q_LCD=As-tu un ecran LCD branche en plus qui sert de DMD ? (o/N) :"
set "en_S6=Start automatically when you sign in to Windows"
set "fr_S6=Lancement automatique a l'ouverture de session Windows"
set "en_Q_AUTO=Turn it on? (Y/n):"
set "fr_Q_AUTO=Activer ? (O/n) :"
set "en_AUTO_OK=Shortcut created in the Startup folder."
set "fr_AUTO_OK=Raccourci cree dans le dossier Demarrage."
set "en_DONE=Setup complete."
set "fr_DONE=Installation terminee."
set "en_T1= - test_pixelcade.bat checks the Pixelcade and its colors"
set "fr_T1= - test_pixelcade.bat verifie la Pixelcade et ses couleurs"
set "en_T2= - screen_setup.bat places the scene on an LCD screen used as a DMD"
set "fr_T2= - screen_setup.bat place la scene sur un ecran LCD qui sert de DMD"
set "en_T3= - demo_afterburner.bat, demo_sonic.bat and demo_fight.bat show the scenes without MAME"
set "fr_T3= - demo_afterburner.bat, demo_sonic.bat et demo_fight.bat montrent les scenes sans MAME"
set "en_T4= - run.bat starts the engine with the console visible"
set "fr_T4= - run.bat demarre le moteur avec la console visible"
set "en_T5= - learn.bat finds the missing RAM addresses (score, credits...)"
set "fr_T5= - learn.bat trouve les adresses RAM manquantes (score, credits...)"
exit /b 0
