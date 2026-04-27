@echo off
setlocal EnableDelayedExpansion

:: ============================================================
:: build_installer.bat
:: Genera Setup_DocAnonymizer.exe en dist\
::
:: Prerequisitos:
::   1. Inno Setup 6 instalado en C:\Program Files (x86)\Inno Setup 6\
::      Descargar: https://jrsoftware.org/isdl.php
::   2. Entorno virtual activado (.venv) con todas las dependencias
::      o Python accesible con las dependencias instaladas
:: ============================================================

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..
set ISCC="%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
set ISS_SCRIPT=%SCRIPT_DIR%doc-anonymizer.iss
set SPEC_FILE=%PROJECT_DIR%\AnonymizerPro.spec

echo.
echo ============================================================
echo  ANON V - Build Installer
echo ============================================================
echo.

:: --- Verificar ISCC ---
if not exist %ISCC% (
    echo [ERROR] Inno Setup Compiler no encontrado en:
    echo         %ISCC%
    echo.
    echo  Instalar desde: https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)

:: --- Paso 1: PyInstaller (onedir) ---
echo [1/2] Ejecutando PyInstaller...
cd /d "%PROJECT_DIR%"
pyinstaller --clean --noconfirm "%SPEC_FILE%"
if errorlevel 1 (
    echo [ERROR] PyInstaller fallo.
    pause
    exit /b 1
)
echo [OK] PyInstaller completado. Carpeta: dist\AnonymizerPro\
echo.

:: --- Paso 2: Inno Setup ---
echo [2/2] Compilando instalador con Inno Setup...
%ISCC% "%ISS_SCRIPT%"
if errorlevel 1 (
    echo [ERROR] Inno Setup fallo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  Instalador generado: dist\Setup_DocAnonymizer.exe
echo ============================================================
echo.
pause
