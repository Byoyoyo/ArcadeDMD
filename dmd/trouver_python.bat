@echo off
rem Trouve un vrai Python 3 et le met dans PY (PYW pour le lancement sans fenetre).
rem Le raccourci "python" du Microsoft Store est ignore, il ne lance rien.
set "PY="
set "PYW="
set "PYDIR="
py -3 -c "import sys" >nul 2>nul
if not "%errorlevel%"=="0" goto try_python
set "PY=py -3"
set "PYW=pyw -3"
goto :eof
:try_python
python -c "import sys" >nul 2>nul
if not "%errorlevel%"=="0" goto try_dirs
set "PY=python"
set "PYW=pythonw"
goto :eof
:try_dirs
for %%V in (315 314 313 312 311 310) do (
  if not defined PYDIR if exist "%LOCALAPPDATA%\Programs\Python\Python%%V\python.exe" set "PYDIR=%LOCALAPPDATA%\Programs\Python\Python%%V"
  if not defined PYDIR if exist "%ProgramFiles%\Python%%V\python.exe" set "PYDIR=%ProgramFiles%\Python%%V"
  if not defined PYDIR if exist "C:\Python%%V\python.exe" set "PYDIR=C:\Python%%V"
)
if not defined PYDIR goto try_launcher
set "PY="%PYDIR%\python.exe""
set "PYW="%PYDIR%\pythonw.exe""
if not exist "%PYDIR%\pythonw.exe" set "PYW=%PY%"
goto :eof
:try_launcher
set "PYL=%LOCALAPPDATA%\Programs\Python\Launcher"
if not exist "%PYL%\py.exe" goto :eof
"%PYL%\py.exe" -3 -c "import sys" >nul 2>nul
if not "%errorlevel%"=="0" goto :eof
set "PY="%PYL%\py.exe" -3"
set "PYW="%PYL%\pyw.exe" -3"
goto :eof
