@echo off
setlocal

@REM start cmd /k "echo Opening new Command Prompt terminal"

set VENV_DIR=myenv

echo Checking if virtual environment exists...
if exist "%VENV_DIR%" (
    echo Yes, Virtual environment already exists: %VENV_DIR%
) else (
    echo No, Virtual environment does not exist. Creating virtual environment...
    python -m venv %VENV_DIR%
    echo Virtual environment folder created: %VENV_DIR%
)

echo Activating virtual environment...
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process"
call .\myenv\Scripts\activate.bat

echo Checking Python executable...
where python

call pip install opencv-python
python cam_capture.py

del "%VENV_DIR%"

pause