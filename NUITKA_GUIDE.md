# 🚀 Nuitka 打包指南

## 📋 什么是Nuitka？

Nuitka是一个Python编译器，它将Python代码编译为C++，然后编译为机器码，提供：
- ⚡ **更快的启动速度** - 比PyInstaller快2-3倍
- 🎯 **更好的运行性能** - 性能提升10-30%
- 📦 **更小的文件大小** - 优化后更紧凑
- 🛡️ **更好的兼容性** - 原生编译

## 🔧 安装和准备

### 1. 安装Nuitka
```bash
# 基础安装
pip install nuitka

# 安装优化依赖
pip install ordered-set

# Windows用户还需要安装C++编译器
# 推荐安装 Visual Studio Build Tools 或 MinGW64
```

### 2. 检查环境
```bash
# 检查Nuitka是否正确安装
python -m nuitka --version

# 检查C++编译器
python -m nuitka --show-scons
```

## 🚀 快速开始

### 方法1: 使用批处理脚本（Windows）
```bash
# 运行简单构建脚本
build_simple.bat
```

### 方法2: 使用Shell脚本（Linux/Mac）
```bash
# 给脚本执行权限
chmod +x build_simple.sh

# 运行构建脚本
./build_simple.sh
```

### 方法3: 使用Python脚本
```bash
# 运行完整的打包脚本
python build_nuitka.py
```

### 方法4: 手动命令
```bash
# 基础编译命令
python -m nuitka \
    --onefile \
    --windows-disable-console \
    --output-filename=PlaneWars \
    --assume-yes-for-downloads \
    --plugin-enable=numpy \
    --include-package=pygame \
    --include-package=numpy \
    main.py
```

## ⚙️ 高级配置

### 🎯 性能优化选项
```bash
python -m nuitka \
    --onefile \
    --lto=yes \
    --enable-plugin=anti-bloat \
    --python-flag=no_asserts \
    --python-flag=no_docstrings \
    --assume-yes-for-downloads \
    main.py
```

### 📦 包含特定模块
```bash
python -m nuitka \
    --onefile \
    --include-module=sound_manager \
    --include-module=config \
    --include-module=player \
    --include-module=enemy \
    --include-module=bullet \
    --include-module=game \
    main.py
```

### 🎨 Windows特定选项
```bash
python -m nuitka \
    --onefile \
    --windows-disable-console \
    --windows-icon-from-ico=icon.ico \
    --windows-company-name="PlaneWars Game" \
    --windows-product-name="PlaneWars" \
    --windows-file-version=1.0.0.0 \
    main.py
```

## 🔍 常用参数说明

### 基础参数
- `--onefile` - 生成单个可执行文件
- `--standalone` - 生成独立目录（包含所有依赖）
- `--output-filename=NAME` - 指定输出文件名
- `--output-dir=DIR` - 指定输出目录

### 优化参数
- `--lto=yes` - 启用链接时优化
- `--enable-plugin=anti-bloat` - 减少文件大小
- `--python-flag=no_asserts` - 禁用断言
- `--python-flag=no_docstrings` - 移除文档字符串

### 包含/排除参数
- `--include-package=PACKAGE` - 强制包含包
- `--include-module=MODULE` - 强制包含模块
- `--plugin-enable=PLUGIN` - 启用插件

### Windows参数
- `--windows-disable-console` - 隐藏控制台窗口
- `--windows-icon-from-ico=FILE` - 设置图标
- `--windows-company-name=NAME` - 设置公司名称

## 🐛 常见问题和解决方案

### 问题1: 找不到模块
```bash
# 解决方案：明确包含模块
--include-module=missing_module
--include-package=missing_package
```

### 问题2: NumPy相关错误
```bash
# 解决方案：启用NumPy插件
--plugin-enable=numpy
```

### 问题3: Pygame音频问题
```bash
# 解决方案：包含pygame的所有子模块
--include-package=pygame
--include-package=pygame.mixer
```

### 问题4: 编译速度慢
```bash
# 解决方案：使用缓存和并行编译
--assume-yes-for-downloads
--jobs=4  # 使用4个并行任务
```

### 问题5: 文件太大
```bash
# 解决方案：启用压缩和优化
--enable-plugin=anti-bloat
--lto=yes
--python-flag=no_docstrings
```

## 📊 性能对比

### 启动时间对比
```
PyInstaller:  ~3-5秒
Nuitka:       ~1-2秒
原生Python:   ~0.5秒
```

### 运行性能对比
```
PyInstaller:  100% (基准)
Nuitka:       110-130%
原生Python:   100%
```

### 文件大小对比
```
PyInstaller:  ~80-120MB
Nuitka:       ~50-80MB
源码:         ~50KB
```

## 🎯 推荐配置

### 开发测试版本
```bash
python -m nuitka \
    --onefile \
    --output-filename=PlaneWars_Debug \
    main.py
```

### 发布版本
```bash
python -m nuitka \
    --onefile \
    --windows-disable-console \
    --lto=yes \
    --enable-plugin=anti-bloat \
    --plugin-enable=numpy \
    --include-package=pygame \
    --output-filename=PlaneWars \
    main.py
```

### 高度优化版本
```bash
python -m nuitka \
    --onefile \
    --windows-disable-console \
    --lto=yes \
    --enable-plugin=anti-bloat \
    --python-flag=no_asserts \
    --python-flag=no_docstrings \
    --plugin-enable=numpy \
    --include-package=pygame \
    --output-filename=PlaneWars_Optimized \
    main.py
```

## 🔧 故障排除

### 查看详细输出
```bash
python -m nuitka --verbose main.py
```

### 检查依赖
```bash
python -m nuitka --show-modules main.py
```

### 测试编译环境
```bash
python -m nuitka --show-scons
```

## 📦 发布准备

### 1. 编译多个版本
- 标准版本（快速编译）
- 优化版本（最佳性能）
- 调试版本（开发用）

### 2. 测试可执行文件
- 在干净的系统上测试
- 检查所有功能是否正常
- 验证性能表现

### 3. 创建发布包
- 包含可执行文件
- 添加说明文档
- 创建压缩包

---

**编译时间**: 首次编译约5-15分钟，后续增量编译更快  
**推荐内存**: 至少4GB RAM  
**推荐存储**: 至少2GB可用空间
