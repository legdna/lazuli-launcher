@echo off
setlocal

REM Configure le PATH pour MSYS2 et Python
set "PATH=C:\msys64\usr\bin;C:\msys64\ucrt64\bin;%PATH%"

REM Exécute le script Python de build
python build.py

endlocal
pause
