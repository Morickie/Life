@echo off
REM 设置Python虚拟环境路径
set VENV_PATH=e:\BaiduSyncdisk\python_promgram\Life\.venv\Scripts\pythonw.exe

REM 设置exercise.py的绝对路径
set EXERCISE_PATH=e:\BaiduSyncdisk\python_promgram\Life\alarm\exercise.py

REM 检查虚拟环境是否存在
if not exist "%VENV_PATH%" (
    echo 虚拟环境未找到，请确保路径正确: %VENV_PATH%
    pause
    exit /b 1
)

REM 检查exercise.py是否存在
if not exist "%EXERCISE_PATH%" (
    echo exercise.py未找到，请确保路径正确: %EXERCISE_PATH%
    pause
    exit /b 1
)

REM 使用start命令在后台运行pythonw.exe，避免黑窗口
start "" "%VENV_PATH%" "%EXERCISE_PATH%"