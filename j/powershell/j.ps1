$winrar = "C:\Program Files\WinRAR\WinRAR.exe"
$archive = "C:\Users\hp\Desktop\j\LOLI TIME.exe"
$chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
$pwd_length = 6
$temp_dir = "C:\Users\hp\Desktop\j\temp_extract"

# 确保临时目录存在
if (-not (Test-Path $temp_dir)) {
    New-Item -Path $temp_dir -ItemType Directory -Force | Out-Null
}

function Generate-RandomPassword {
    param ([int]$length)
    $password = ""
    for ($i = 0; $i -lt $length; $i++) {
        $idx = Get-Random -Minimum 0 -Maximum $chars.Length
        $password += $chars[$idx]
    }
    return $password
}

$i = 0
while ($true) {
    # 清空临时目录内容
    Remove-Item -Path "$temp_dir\*" -Force -Recurse -ErrorAction SilentlyContinue

    # 生成随机密码
    $password = Generate-RandomPassword -length $pwd_length

    try {
        # 尝试解压文件并隐藏窗口
        $process = Start-Process -FilePath $winrar -ArgumentList "x -p$password -inul `"$archive`" `"$temp_dir`"" -WindowStyle Hidden -PassThru -ErrorAction Stop

        # 等待进程完成并检查退出代码
        if ($process -ne $null) {
            $process.WaitForExit()
            if ($process.ExitCode -eq 0) {
                Write-Host "Password is correct: $password"
                break
            }
        } else {
            Write-Host "Failed to start process with password: $password"
        }
    } catch {
        Write-Host "An error occurred while trying the password: $password"
        Write-Host "Error details: $_"
    }

    # 增大输出频率
    Write-Host "Trying password: $password"

    $i++
}

# 清理临时文件夹
Remove-Item -Path "$temp_dir" -Force -Recurse -ErrorAction SilentlyContinue

# 暂停以便查看结果
Read-Host "Press Enter to exit"