@echo off
echo 🚀 飞机大战游戏 Nuitka 快速打包
echo ================================

echo 📦 安装Nuitka...
pip install nuitka

echo 🧹 清理旧文件...
if exist "main.exe" del "main.exe"
if exist "PlaneWars.exe" del "PlaneWars.exe"
if exist "main.build" rmdir /s /q "main.build"
if exist "main.dist" rmdir /s /q "main.dist"

echo 🔨 开始编译...
python -m nuitka ^
    --onefile ^
    --windows-disable-console ^
    --output-filename=PlaneWars ^
    --assume-yes-for-downloads ^
    --plugin-enable=numpy ^
    --include-package=pygame ^
    --include-package=numpy ^
    --include-module=sound_manager ^
    --include-module=config ^
    --include-module=player ^
    --include-module=enemy ^
    --include-module=bullet ^
    --include-module=game ^
    main.py

if exist "PlaneWars.exe" (
    echo ✅ 编译成功！
    echo 📁 可执行文件: PlaneWars.exe
    echo 📊 文件大小:
    dir PlaneWars.exe
) else (
    echo ❌ 编译失败！
)

pause
