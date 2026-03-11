@echo off
call .venv\Scripts\activate.bat
pip install scipy
pip list | findstr scipy
