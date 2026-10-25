@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"
echo ==============================================
echo   Installation ArcadeDMD
echo ==============================================
echo.

rem ---------- 1. Python et bibliotheques ----------
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY (
  echo Python est introuvable.
  echo Installe Python 3.12 ou plus recent depuis https://www.python.org/downloads/
  echo en cochant "Add python.exe to PATH", puis relance installer.bat.
  pause
  exit /b 1
)
echo [1/5] Bibliotheques Python
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
if !TRIES! GTR 5 (
  echo   Trop d'essais. Relance installer.bat quand tu connais le dossier de MAME.
  pause
  exit /b 1
)
set "ANS="
if defined MAMEDIR echo   MAME trouve dans !MAMEDIR!. Appuie sur Entree pour le garder.
set /p "ANS=  Dossier de MAME, celui qui contient mame.exe : "
if defined ANS set "ANS=!ANS:"=!"
if defined ANS set "MAMEDIR=!ANS!"
if not defined MAMEDIR goto ask_mame
%PY% arcadedmd.py install-plugin "!MAMEDIR!"
if errorlevel 2 (
  pause
  exit /b 1
)
if errorlevel 1 (
  set "MAMEDIR="
  echo   Indique le bon dossier, ou ferme cette fenetre pour abandonner.
  goto ask_mame
)

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
set "PYW=pythonw"
where pyw >nul 2>nul && set "PYW=pyw -3"
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
