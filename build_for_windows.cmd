@echo off
setlocal

REM Configure le PATH pour MSYS2 et Python
set "PATH=C:\msys64\usr\bin;C:\msys64\ucrt64\bin;%PATH%"

REM Complilation du fichier gresource
glib-compile-resources --target=data/oracles.gresource --sourcedir=data "data/oracles.gresource.xml"

REM Exécute le script Python de build
REM python build.py
pyinstaller oracles.spec

endlocal
pause
