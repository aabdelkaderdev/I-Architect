@echo off
REM ──────────────────────────────────────────────────────────────
REM download_model.bat — Download and extract ARLO embedding models
REM ──────────────────────────────────────────────────────────────
REM Downloads models.7z from Google Drive and extracts it into arlo\
REM
REM Prerequisites:
REM   - pip install gdown
REM   - 7-Zip installed and on PATH  (https://www.7-zip.org)
REM
REM Usage:
REM   download_model.bat
REM ──────────────────────────────────────────────────────────────

setlocal enabledelayedexpansion

set "GDRIVE_FILE_ID=1bQNQgDd-O8bb1XCuT0T9Ji-YYKqtH9Or"
set "ARCHIVE_NAME=models.7z"
set "EXTRACT_DIR=arlo"

cd /d "%~dp0"

REM ── Dependency checks ──────────────────────────────────────
where 7z >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 7z not found. Install 7-Zip and add it to PATH:
    echo         https://www.7-zip.org
    echo.
    echo     Default install path to add to PATH:
    echo         C:\Program Files\7-Zip
    exit /b 1
)

where gdown >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] gdown not found — installing via pip...
    pip install --quiet gdown
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install gdown. Make sure Python and pip are on PATH.
        exit /b 1
    )
)

REM ── Download ───────────────────────────────────────────────
if exist "%ARCHIVE_NAME%" (
    echo [OK] %ARCHIVE_NAME% already exists, skipping download.
) else (
    echo [DOWNLOAD] Downloading %ARCHIVE_NAME% from Google Drive...
    gdown --id %GDRIVE_FILE_ID% -O %ARCHIVE_NAME%
    if %errorlevel% neq 0 (
        echo [ERROR] Download failed.
        exit /b 1
    )
)

REM ── Extract ────────────────────────────────────────────────
echo [EXTRACT] Extracting %ARCHIVE_NAME% into %EXTRACT_DIR%\ ...
7z x "%ARCHIVE_NAME%" -o"%EXTRACT_DIR%" -aoa -y
if %errorlevel% neq 0 (
    echo [ERROR] Extraction failed.
    exit /b 1
)

echo.
echo [OK] Done! Models extracted to %EXTRACT_DIR%\models\

endlocal
