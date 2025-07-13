@echo off
echo 🚀 启动飞机大战游戏...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖是否安装
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo 📦 正在安装游戏依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM 启动游戏
echo ✅ 启动游戏中...
python src/main.py

echo.
echo 🎮 游戏已退出
pause
