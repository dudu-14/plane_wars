#!/bin/bash

echo "🚀 启动飞机大战游戏..."
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查依赖是否安装
python3 -c "import pygame" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 正在安装游戏依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，请手动运行: pip3 install -r requirements.txt"
        exit 1
    fi
fi

# 启动游戏
echo "✅ 启动游戏中..."
python3 src/main.py

echo
echo "🎮 游戏已退出"
