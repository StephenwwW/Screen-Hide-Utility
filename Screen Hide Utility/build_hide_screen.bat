@echo off
setlocal enabledelayedexpansion

set SCRIPT=C:\Users\H\Desktop\hide_screen.py.py
set UPX=C:\Users\H\Desktop\upx-5.0.1-win64
set OUTPUT_NAME=hide_screen.py.exe
set OUTPUT_DIR=%USERPROFILE%\Desktop
set WORKDIR=%~dp0

echo ----------------------------------------
echo PyInstaller Build Script for hide_screen.py.py
echo.
echo Choose the build method:
echo 1 - pyinstaller --onefile --noconsole --upx-dir
echo 2 - pyinstaller --onefile --noconsole (no UPX)
echo 3 - pyinstaller --onefile --noconsole --strip --clean --upx-dir
echo.
set /p choice=Enter your choice (1/2/3): 

if "%choice%"=="1" (
    echo Running: pyinstaller --onefile --noconsole --upx-dir "%UPX%" "%SCRIPT%"
    pyinstaller --onefile --noconsole --upx-dir "%UPX%" "%SCRIPT%"
) else if "%choice%"=="2" (
    echo Running: pyinstaller --onefile --noconsole "%SCRIPT%"
    pyinstaller --onefile --noconsole "%SCRIPT%"
) else if "%choice%"=="3" (
    echo Running: pyinstaller --onefile --noconsole --strip --clean --upx-dir "%UPX%" "%SCRIPT%"
    pyinstaller --onefile --noconsole --strip --clean --upx-dir "%UPX%" "%SCRIPT%"
) else (
    echo Invalid choice. Exiting.
    goto :eof
)

REM 確認並移動exe到桌面
set DIST_PATH=%WORKDIR%dist\%OUTPUT_NAME%

if exist "%DIST_PATH%" (
    echo.
    echo Moving %DIST_PATH% to %OUTPUT_DIR%
    move /y "%DIST_PATH%" "%OUTPUT_DIR%"
) else (
    echo ERROR: Build output file not found: %DIST_PATH%
    goto :cleanup
)

:cleanup
REM 刪除build資料夾
if exist "%WORKDIR%build" (
    echo Removing build folder...
    rmdir /s /q "%WORKDIR%build"
)

REM 刪除dist資料夾（已搬走exe）
if exist "%WORKDIR%dist" (
    echo Removing dist folder...
    rmdir /s /q "%WORKDIR%dist"
)

REM 刪除 .spec 文件 (修正檔案名稱)
set SPEC_FILE=%WORKDIR%hide_screen.py.spec
if exist "%SPEC_FILE%" (
    echo Removing spec file...
    del /f /q "%SPEC_FILE%"
)

echo.
echo Build finished! Only %OUTPUT_NAME% should remain on your desktop.
pause
endlocal