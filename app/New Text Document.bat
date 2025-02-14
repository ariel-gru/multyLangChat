@echo off
echo Starting Server...
start cmd.exe /k "python C:\Users\Ariel\Documents\Codind_Projects\cyber_project\app\server.py"

timeout /t 2 /nobreak

echo Starting Client...
start cmd.exe /k "python C:\Users\Ariel\Documents\Codind_Projects\cyber_project\app\client.py"
