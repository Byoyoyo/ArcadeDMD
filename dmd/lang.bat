@echo off
rem Sets L=en or L=fr for the messages of the .bat files, with the same rule as ArcadeDMD itself:
rem "language" in config.json ("en" or "fr"), then the ARCADEDMD_LANG variable, then the Windows display language.
rem Choisit la langue des messages des .bat (L=en ou L=fr), avec la meme regle qu'ArcadeDMD :
rem "language" dans config.json, puis la variable ARCADEDMD_LANG, puis la langue d'affichage de Windows.
set "L="
set "LCFG=%~dp0..\config.json"
if not exist "%LCFG%" goto lang_env
for /f "usebackq tokens=1,2 delims={:, " %%A in ("%LCFG%") do if /i "%%~A"=="language" set "L=%%~B"
if /i "%L:~0,2%"=="fr" goto lang_done
if /i "%L:~0,2%"=="en" goto lang_done
set "L="
:lang_env
if not defined ARCADEDMD_LANG goto lang_windows
set "L=%ARCADEDMD_LANG:~0,2%"
if /i "%L%"=="fr" goto lang_done
if /i "%L%"=="en" goto lang_done
set "L="
:lang_windows
for /f "usebackq delims=" %%A in (`powershell -NoProfile -NonInteractive -Command "[Globalization.CultureInfo]::CurrentUICulture.TwoLetterISOLanguageName" 2^>nul`) do set "L=%%A"
if defined L goto lang_done
for /f "tokens=3" %%A in ('reg query "HKCU\Control Panel\International" /v LocaleName 2^>nul ^| findstr /i "LocaleName"') do set "L=%%A"
:lang_done
set "LCFG="
if /i "%L:~0,2%"=="fr" (set "L=fr") else (set "L=en")
goto :eof
