# 📁 项目结构说明

## 🏗️ 目录结构

```
plane_wars/
├── 📁 src/                     # 源代码目录
│   ├── main.py                 # 游戏主入口
│   ├── game.py                 # 游戏主逻辑
│   ├── player.py               # 玩家飞机类
│   ├── enemy.py                # 敌机类
│   ├── bullet.py               # 子弹类
│   ├── sound_manager.py        # 音效管理
│   └── config.py               # 游戏配置
├── 📁 docs/                    # 文档目录
│   ├── API_REFERENCE.md        # API参考文档
│   ├── CHANGELOG.md            # 更新日志
│   ├── DEVELOPER_GUIDE.md      # 开发者指南
│   ├── NUITKA_GUIDE.md         # Nuitka编译指南
│   ├── RELEASE_NOTES_v1.0.0.md # 发布说明
│   ├── 需求.md                 # 项目需求文档
│   └── 需求1.1.md              # 需求更新文档
├── 📁 scripts/                 # 构建脚本目录
│   ├── build_nuitka.py         # Nuitka编译脚本
│   ├── build_simple.bat        # 简单构建脚本(Windows)
│   └── build_simple.sh         # 简单构建脚本(Linux/Mac)
├── 📁 tests/                   # 测试文件目录
│   ├── test_font.py            # 字体测试
│   └── test_game.py            # 游戏测试
├── 📁 releases/                # 发布文件目录
│   └── release_clean/          # 清理后的发布文件
│       ├── PlaneWars_Basic.exe
│       ├── main.dist/
│       ├── PlaneWars_v1.0.0_Nuitka_Windows_x64.zip
│       └── README_编译版本.txt
├── README.md                   # 项目说明文档
├── requirements.txt            # Python依赖列表
└── PROJECT_STRUCTURE.md        # 本文件
```

## 📋 目录说明

### 📁 src/ - 源代码目录
包含所有游戏源代码文件：
- **main.py** - 游戏启动入口点
- **game.py** - 游戏主循环和逻辑控制
- **player.py** - 玩家飞机的实现
- **enemy.py** - 敌机的实现
- **bullet.py** - 子弹系统的实现
- **sound_manager.py** - 音效管理系统
- **config.py** - 游戏配置和常量

### 📁 docs/ - 文档目录
包含所有项目文档：
- **API_REFERENCE.md** - 代码API参考
- **CHANGELOG.md** - 版本更新记录
- **DEVELOPER_GUIDE.md** - 开发者使用指南
- **NUITKA_GUIDE.md** - Nuitka编译详细指南
- **RELEASE_NOTES_v1.0.0.md** - v1.0.0版本发布说明
- **需求.md** - 原始项目需求
- **需求1.1.md** - 需求更新文档

### 📁 scripts/ - 构建脚本目录
包含各种构建和编译脚本：
- **build_nuitka.py** - 完整的Nuitka编译脚本
- **build_simple.bat** - Windows简单编译脚本
- **build_simple.sh** - Linux/Mac简单编译脚本

### 📁 tests/ - 测试目录
包含测试文件：
- **test_font.py** - 字体相关测试
- **test_game.py** - 游戏功能测试

### 📁 releases/ - 发布目录
包含编译后的发布文件：
- **release_clean/** - 整理后的发布文件夹
  - 包含所有可执行文件和依赖
  - 包含发布压缩包
  - 包含使用说明

## 🚀 使用说明

### 开发环境
```bash
# 安装依赖
pip install -r requirements.txt

# 运行游戏
python src/main.py

# 运行测试
python tests/test_game.py
```

### 编译发布
```bash
# 使用Nuitka编译
python scripts/build_nuitka.py

# 或使用简单脚本
scripts/build_simple.bat  # Windows
scripts/build_simple.sh   # Linux/Mac
```

### 发布文件
编译后的文件位于 `releases/release_clean/` 目录中，可直接分发使用。

## 📝 维护说明

- **源代码** 放在 `src/` 目录
- **文档** 放在 `docs/` 目录  
- **脚本** 放在 `scripts/` 目录
- **测试** 放在 `tests/` 目录
- **发布** 放在 `releases/` 目录

这样的结构使项目更加清晰和易于维护。
