@echo off
chcp 65001 >nul
setlocal

:: מקבל את שם המשתמש הנוכחי
set "USERNAME=%USERNAME%"

:: בונה את הנתיב לפי היוזר
set "PLUGIN_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\Lib\site-packages\PyQt5\Qt5\plugins"

:: מגדיר את משתנה QT_PLUGIN_PATH
setx QT_PLUGIN_PATH "%PLUGIN_PATH%"

echo -----------------------------------
echo QT_PLUGIN_PATH הוגדר ל:
echo %PLUGIN_PATH%
echo -----------------------------------
pause
