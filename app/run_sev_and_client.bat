@echo off
cd /d "%~dp0app"
start "" python server.py
start "" python chatappGUI.py
