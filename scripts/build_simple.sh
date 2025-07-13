#!/bin/bash

echo "🚀 飞机大战游戏 Nuitka 快速打包"
echo "================================"

echo "📦 安装Nuitka..."
pip install nuitka

echo "🧹 清理旧文件..."
rm -f main PlaneWars
rm -rf main.build main.dist

echo "🔨 开始编译..."
python -m nuitka \
    --onefile \
    --output-filename=PlaneWars \
    --assume-yes-for-downloads \
    --plugin-enable=numpy \
    --include-package=pygame \
    --include-package=numpy \
    --include-module=sound_manager \
    --include-module=config \
    --include-module=player \
    --include-module=enemy \
    --include-module=bullet \
    --include-module=game \
    main.py

if [ -f "PlaneWars" ]; then
    echo "✅ 编译成功！"
    echo "📁 可执行文件: PlaneWars"
    echo "📊 文件大小:"
    ls -lh PlaneWars
    echo ""
    echo "🎮 运行游戏: ./PlaneWars"
else
    echo "❌ 编译失败！"
fi
