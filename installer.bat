@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
set "ROOT=%~dp0"
if not exist config.json copy /y config.defaut.json config.json >nul
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"
echo ==============================================
echo   Installation ArcadeDMD
echo ==============================================
echo.

rem ---------- 1. Python et bibliotheques ----------
call "%~dp0dmd\trouver_python.bat"
if defined PY goto python_ok
echo Python n'est pas installe sur ce PC.
echo Le raccourci "python" du Microsoft Store ne compte pas, il ne lance rien.
where winget >nul 2>nul
if errorlevel 1 goto python_manual
set "ANS="
set /p "ANS=  Installer Python 3.13 maintenant depuis python.org ? (O/n) : "
if /i "!ANS!"=="n" goto python_manual
winget install -e --id Python.Python.3.13 --scope user --accept-package-agreements --accept-source-agreements
call "%~dp0dmd\trouver_python.bat"
if defined PY goto python_ok
:python_manual
echo Installe Python 3.13 depuis https://www.python.org/downloads/ en cochant "Add python.exe to PATH",
echo puis relance installer.bat.
pause
exit /b 1
:python_ok
echo [1/5] Bibliotheques Python
echo   Python utilise !PY!
%PY% -m pip install --upgrade pillow pyserial
if errorlevel 1 (
  echo Echec de l'installation de Pillow ou pyserial. Verifie la connexion internet puis relance.
  pause
  exit /b 1
)
%PY% -c "import pygame" >nul 2>nul
if errorlevel 1 (
  %PY% -m pip install --upgrade pygame-ce
  if errorlevel 1 echo   pygame-ce non installe : la fenetre LED virtuelles utilisera tkinter, plus lente.
) else (
  echo   pygame deja present.
)

rem ---------- 2. ZeDMD (facultatif) ----------
echo.
echo [2/5] Dalle ZeDMD
echo   Seulement si tu as une dalle ZeDMD en plus. Avec une Pixelcade seule, appuie sur Entree.
set "ANS="
set /p "ANS=  As-tu une dalle ZeDMD ? (o/N) : "
if /i not "!ANS!"=="o" (
  echo   Pas de ZeDMD, etape ignoree.
  goto zedmd_done
)
%PY% arcadedmd.py check-zedmd >nul 2>nul
if errorlevel 1 (
  set "ZVER=0.11.0"
  set "ZURL=https://github.com/PPUC/libzedmd/releases/download/v!ZVER!/libzedmd-!ZVER!-win-mingw-x64-Release.zip"
  echo   Telechargement de !ZURL!
  curl -L -f -s -o "%TEMP%\libzedmd.zip" "!ZURL!"
  if errorlevel 1 (
    echo   Telechargement impossible.
  ) else (
    if not exist libzedmd mkdir libzedmd
    tar -xf "%TEMP%\libzedmd.zip" -C libzedmd
  )
)
%PY% arcadedmd.py check-zedmd
if errorlevel 1 (
  echo   Recupere a la main l'archive "win-mingw-x64-Release" sur https://github.com/PPUC/libzedmd/releases
  echo   et copie toutes ses DLL dans le dossier libzedmd d'ArcadeDMD.
)
%PY% arcadedmd.py enable-zedmd
:zedmd_done

rem ---------- 3. Plugin MAME ----------
echo.
echo [3/5] Plugin MAME
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
if defined MAMEDIR echo   MAME trouve dans !MAMEDIR!. Appuie sur Entree pour le garder.
if not defined MAMEDIR echo   Si tu n'utilises pas MAME ^(seulement RetroArch^), appuie simplement sur Entree.
set /p "ANS=  Dossier de MAME, celui qui contient mame.exe : "
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
  echo   Indique le bon dossier, ou appuie sur Entree pour passer.
  goto ask_mame
)
goto mame_done
:skip_mame
echo   Plugin MAME non installe. Relance installer.bat le jour ou tu veux l'utiliser avec MAME.
:mame_done

rem ---------- 4. Pixelcade ----------
echo.
echo [4/5] Pixelcade LED
set "ANS="
set /p "ANS=  As-tu une Pixelcade LED a piloter ? (o/N) : "
if /i "!ANS!"=="o" %PY% arcadedmd.py setup-pixelcade

rem ---------- 5. Demarrage automatique ----------
echo.
echo [5/5] Lancement automatique a l'ouverture de session Windows
set "ANS="
set /p "ANS=  Activer ? (O/n) : "
if /i "!ANS!"=="n" goto done
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
> "!STARTUP!\ArcadeDMD.bat" echo @echo off
>> "!STARTUP!\ArcadeDMD.bat" echo cd /d "!ROOT!"
>> "!STARTUP!\ArcadeDMD.bat" echo start "" !PYW! "!ROOT!\arcadedmd.py"
echo   Raccourci cree dans le dossier Demarrage.

:done
echo.
echo Installation terminee.
echo  - test_pixelcade.bat verifie la Pixelcade et ses couleurs
echo  - demo_afterburner.bat et demo_sonic.bat montrent les scenes sans MAME
echo  - lancer.bat demarre le moteur avec la console visible
echo  - apprendre.bat trouve les adresses RAM manquantes ^(After Burner II^)
echo.
pause
