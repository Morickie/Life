@echo off
REM 设置Python虚拟环境路径
set VENV_PATH=e:\BaiduSyncdisk\python_promgram\Life\.venv\Scripts\pythonw.exe

REM 设置focus_break_reminder.py的绝对路径
set REMINDER_PATH=e:\BaiduSyncdisk\python_promgram\Life\work_focus\focus_break_reminder.py

REM 检查虚拟环境是否存在
if not exist "%VENV_PATH%" (
    echo 虚拟环境未找到，请确保路径正确: %VENV_PATH%
    pause
    exit /b 1
)

REM 检查focus_break_reminder.py是否存在
if not exist "%REMINDER_PATH%" (
    echo focus_break_reminder.py未找到，请确保路径正确: %REMINDER_PATH%
    pause
    exit /b 1
)

REM 使用start命令在后台运行pythonw.exe，避免黑窗口
start "" "%VENV_PATH%" "%REMINDER_PATH%"