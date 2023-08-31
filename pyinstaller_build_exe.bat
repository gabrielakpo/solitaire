
pushd %~dp0
if exist build RMDIR /S /Q build
if exist dist RMDIR /S /Q dist
pyinstaller .\pyinstaller_build_exe.spec