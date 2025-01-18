@echo off
setlocal enabledelayedexpansion

:: 设置WinRAR路径（确保指向WinRAR.exe而不是快捷方式）
set "winrar=C:\Program Files\WinRAR\WinRAR.exe"

:: 设置自解压文件路径
set "archive=C:\Users\hp\Desktop\j\LOLI TIME.exe"

:: 设置要尝试的字符集 (A-Z, 0-9)，密码长度
set "chars=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
set pwd_length=6

:: 创建一个固定临时目录存放解压结果，减少频繁创建和删除临时文件夹
set "temp_dir=C:\Users\hp\Desktop\j\temp_extract"
if not exist "%temp_dir%" mkdir "%temp_dir%" >nul 2>&1

:loop
:: 清空临时目录内容
del /q "%temp_dir%\*" >nul 2>&1

:: 生成随机密码
set "password="
for /L %%i in (1,1,%pwd_length%) do (
    set /A idx=!random! %% 36
    for %%j in (!idx!) do (
        set "password=!password!!chars:~%%j,1!"
    )
)
:: set "password=Y7UMKB"
:: echo Trying password: !password!

:: 尝试解压文件并重定向所有流以隐藏窗口
"%winrar%" x -p!password! -inul "%archive%" "%temp_dir%\" >nul 2>&1

:: 检查命令执行的状态码
if !ERRORLEVEL! EQU 0 (
    echo Password is correct: !password!
    goto :cleanup
) else (
    :: echo Password incorrect: !password!
    goto :loop
)

:cleanup
:: 清理临时文件夹 (可选)
:: rmdir /s /q "%temp_dir%" >nul 2>&1
endlocal
pause