@echo off
echo 🚀 飞机大战游戏 v1.1.0 Nuitka 编译
echo ====================================

echo 🧹 清理旧文件...
if exist "PlaneWars_v1.1.0.exe" del "PlaneWars_v1.1.0.exe"
if exist "main.build" rmdir /s /q "main.build"
if exist "main.dist" rmdir /s /q "main.dist"
if exist "dist" rmdir /s /q "dist"

echo 🔨 开始编译 v1.1.0 版本...
python -m nuitka ^
    --onefile ^
    --windows-disable-console ^
    --output-filename=PlaneWars_v1.1.0 ^
    --assume-yes-for-downloads ^
    --plugin-enable=numpy ^
    --include-package=pygame ^
    --include-package=numpy ^
    --include-module=sound_manager ^
    --include-module=config ^
    --include-module=player ^
    --include-module=enemy ^
    --include-module=bullet ^
    --include-module=item ^
    --include-module=game ^
    --windows-company-name="PlaneWars Game" ^
    --windows-product-name="PlaneWars v1.1.0" ^
    --windows-file-version=1.1.0.0 ^
    --windows-product-version=1.1.0 ^
    --windows-file-description="飞机大战游戏 v1.1.0" ^
    main.py

if exist "PlaneWars_v1.1.0.exe" (
    echo ✅ 编译成功！
    echo 📁 可执行文件: PlaneWars_v1.1.0.exe
    echo 📊 文件大小:
    dir PlaneWars_v1.1.0.exe
    
    echo 📦 创建发布目录...
    if not exist "..\releases\release_clean_v1.1.0" mkdir "..\releases\release_clean_v1.1.0"
    copy "PlaneWars_v1.1.0.exe" "..\releases\release_clean_v1.1.0\"
    copy "..\README.md" "..\releases\release_clean_v1.1.0\"
    copy "..\docs\CHANGELOG.md" "..\releases\release_clean_v1.1.0\"
    copy "..\requirements.txt" "..\releases\release_clean_v1.1.0\"
    
    echo ✅ 发布包创建完成！
    echo 📂 发布目录: ..\releases\release_clean_v1.1.0\
) else (
    echo ❌ 编译失败！
)

pause
