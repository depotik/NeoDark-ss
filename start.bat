@echo off
cd /d "%~dp0"

:: Check Python installation
python --version >nul 2>nul
if errorlevel 1 goto nopython

:: Run main program
cmd /k python main.py
exit /b

:nopython
echo ERROR: Python not found!
echo.
echo Please install Python from:
echo https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe
echo.
echo Don't forget to check "Add Python to PATH" during installation.
echo.
echo Opening download page...
start https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe
echo.
pause
exit /b