# 飞机大战游戏 API 参考文档

## 📚 模块概览

### 核心模块
- [`game.py`](#game-module) - 游戏主控制器
- [`player.py`](#player-module) - 玩家飞机类
- [`enemy.py`](#enemy-module) - 敌机类
- [`bullet.py`](#bullet-module) - 子弹类
- [`sound_manager.py`](#sound-manager-module) - 音效管理器
- [`config.py`](#config-module) - 配置常量

---

## 🎮 Game Module

### Class: `Game`

游戏主控制器类，负责管理整个游戏的运行。

#### 构造函数
```python
def __init__(self) -> None
```
初始化游戏，创建窗口、玩家、字体和音效管理器。

#### 属性
```python
screen: pygame.Surface          # 游戏主窗口
clock: pygame.time.Clock        # 游戏时钟
running: bool                   # 游戏是否运行中
game_over: bool                 # 游戏是否结束
score: int                      # 当前分数
player: Player                  # 玩家对象
enemies: List[Enemy]            # 敌机列表
player_bullets: List[Bullet]    # 玩家子弹列表
enemy_bullets: List[Bullet]     # 敌机子弹列表
sound_manager: SoundManager     # 音效管理器
```

#### 主要方法

##### `run() -> None`
启动游戏主循环。

##### `handle_events() -> None`
处理用户输入和系统事件。

**处理的事件:**
- `pygame.QUIT` - 退出游戏
- `pygame.K_SPACE` - 发射子弹（非自动模式）
- `pygame.K_r` - 重新开始游戏

##### `update_game() -> None`
更新游戏状态，包括玩家、敌机、子弹的位置和状态。

##### `check_collisions() -> None`
检查所有碰撞并处理相应逻辑。

**碰撞类型:**
- 玩家子弹 vs 敌机
- 敌机子弹 vs 玩家
- 敌机 vs 玩家

##### `spawn_enemies() -> None`
根据概率随机生成敌机。

**生成规则:**
- 70% 概率生成小型敌机
- 30% 概率生成中型敌机

##### `draw() -> None`
渲染游戏画面，包括所有游戏对象和UI元素。

##### `restart_game() -> None`
重置游戏状态，重新开始游戏。

---

## 🛩️ Player Module

### Class: `Player`

玩家飞机类，处理玩家控制和状态管理。

#### 构造函数
```python
def __init__(self, x: int, y: int) -> None
```

**参数:**
- `x` - 初始x坐标
- `y` - 初始y坐标

#### 属性
```python
x: int                    # x坐标位置
y: int                    # y坐标位置
width: int                # 飞机宽度
height: int               # 飞机高度
speed: int                # 移动速度
lives: int                # 剩余生命值
last_bullet_time: float   # 上次发射时间
rect: pygame.Rect         # 碰撞检测矩形
```

#### 主要方法

##### `update(keys_pressed: pygame.key.ScancodeWrapper) -> None`
根据键盘输入更新玩家位置。

**支持的按键:**
- `pygame.K_LEFT` - 向左移动
- `pygame.K_RIGHT` - 向右移动
- `pygame.K_UP` - 向上移动
- `pygame.K_DOWN` - 向下移动

##### `shoot() -> Optional[Tuple[int, int]]`
发射子弹，返回子弹初始位置。

**返回值:**
- `Tuple[int, int]` - 子弹位置 (x, y)
- `None` - 冷却中，无法发射

##### `can_shoot() -> bool`
检查是否可以发射子弹（冷却时间检查）。

##### `take_damage() -> None`
受到伤害，生命值减1。

##### `is_alive() -> bool`
检查玩家是否还活着。

##### `draw(screen: pygame.Surface) -> None`
在屏幕上绘制玩家飞机。

---

## 👾 Enemy Module

### Class: `Enemy`

敌机类，支持不同类型的敌机。

#### 构造函数
```python
def __init__(self, x: int, y: int, enemy_type: EnemyType = "small") -> None
```

**参数:**
- `x` - 初始x坐标
- `y` - 初始y坐标
- `enemy_type` - 敌机类型 ("small" | "medium")

#### 属性
```python
enemy_type: str           # 敌机类型
x: int                    # x坐标位置
y: int                    # y坐标位置
width: int                # 敌机宽度
height: int               # 敌机高度
speed: int                # 移动速度
hp: int                   # 当前生命值
max_hp: int               # 最大生命值
score: int                # 击毁奖励分数
color: Tuple[int,int,int] # 敌机颜色
rect: pygame.Rect         # 碰撞检测矩形
```

#### 敌机类型配置

##### Small Enemy (小型敌机)
```python
width: 40px
height: 30px
speed: 2px/frame
hp: 1
score: 10
color: RED
```

##### Medium Enemy (中型敌机)
```python
width: 60px
height: 45px
speed: 1px/frame
hp: 2
score: 30
color: DARK_RED
```

#### 主要方法

##### `update() -> None`
更新敌机位置（向下移动）。

##### `is_off_screen() -> bool`
检查敌机是否飞出屏幕。

##### `shoot() -> Optional[Tuple[int, int]]`
随机发射子弹。

**发射概率:**
- 小型敌机: 0.5%/帧
- 中型敌机: 1.0%/帧

##### `take_damage() -> None`
受到伤害，生命值减1。

##### `is_alive() -> bool`
检查敌机是否还活着。

##### `draw(screen: pygame.Surface) -> None`
绘制敌机，包括血量条（如果受伤）。

---

## 🔫 Bullet Module

### Class: `Bullet`

子弹类，支持玩家和敌机子弹。

#### 构造函数
```python
def __init__(self, x: int, y: int, bullet_type: BulletType = "player") -> None
```

**参数:**
- `x` - 初始x坐标
- `y` - 初始y坐标
- `bullet_type` - 子弹类型 ("player" | "enemy")

#### 属性
```python
x: int                    # x坐标位置
y: int                    # y坐标位置
width: int                # 子弹宽度
height: int               # 子弹高度
bullet_type: str          # 子弹类型
speed: int                # 移动速度（带方向）
color: Tuple[int,int,int] # 子弹颜色
rect: pygame.Rect         # 碰撞检测矩形
```

#### 子弹类型配置

##### Player Bullet (玩家子弹)
```python
speed: -8px/frame  # 向上移动
color: YELLOW
```

##### Enemy Bullet (敌机子弹)
```python
speed: 4px/frame   # 向下移动
color: RED
```

#### 主要方法

##### `update() -> None`
更新子弹位置。

##### `is_off_screen() -> bool`
检查子弹是否飞出屏幕。

##### `draw(screen: pygame.Surface) -> None`
绘制子弹。

---

## 🔊 Sound Manager Module

### Class: `SoundManager`

音效管理器类，负责游戏音效的生成和播放。

#### 构造函数
```python
def __init__(self, enabled: bool = True, volume: float = 0.5) -> None
```

**参数:**
- `enabled` - 是否启用音效
- `volume` - 音效音量 (0.0-1.0)

#### 属性
```python
enabled: bool                           # 音效是否启用
volume: float                           # 音效音量
sounds: Dict[str, pygame.mixer.Sound]   # 音效字典
```

#### 音效类型

##### 可用音效
- `shoot` - 射击音效
- `enemy_kill` - 击杀音效
- `player_hit` - 受击音效
- `enemy_spawn` - 敌机出现音效

#### 主要方法

##### `play_shoot() -> None`
播放射击音效。

##### `play_enemy_kill() -> None`
播放敌机击杀音效。

##### `play_player_hit() -> None`
播放玩家受击音效。

##### `play_enemy_spawn() -> None`
播放敌机出现音效。

##### `set_volume(volume: float) -> None`
设置音效音量。

##### `toggle_sound() -> None`
切换音效开关。

##### `is_enabled() -> bool`
检查音效是否启用。

---

## ⚙️ Config Module

### 配置常量

#### 屏幕设置
```python
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60
```

#### 颜色定义
```python
BLACK: tuple = (0, 0, 0)
WHITE: tuple = (255, 255, 255)
RED: tuple = (255, 0, 0)
GREEN: tuple = (0, 255, 0)
BLUE: tuple = (0, 0, 255)
YELLOW: tuple = (255, 255, 0)
GRAY: tuple = (128, 128, 128)
DARK_RED: tuple = (150, 0, 0)
```

#### 玩家配置
```python
PLAYER_WIDTH: int = 60
PLAYER_HEIGHT: int = 80
PLAYER_SPEED: int = 5
PLAYER_INITIAL_LIVES: int = 9999999999
BULLET_COOLDOWN: float = 0.001
AUTO_FIRE: bool = True
```

#### 敌机配置
```python
# 小型敌机
ENEMY_SMALL_WIDTH: int = 40
ENEMY_SMALL_HEIGHT: int = 30
ENEMY_SMALL_SPEED: int = 2
ENEMY_SMALL_HP: int = 1
ENEMY_SMALL_SCORE: int = 10

# 中型敌机
ENEMY_MEDIUM_WIDTH: int = 60
ENEMY_MEDIUM_HEIGHT: int = 45
ENEMY_MEDIUM_SPEED: int = 1
ENEMY_MEDIUM_HP: int = 2
ENEMY_MEDIUM_SCORE: int = 30
```

#### 子弹配置
```python
BULLET_WIDTH: int = 4
BULLET_HEIGHT: int = 10
PLAYER_BULLET_SPEED: int = 8
ENEMY_BULLET_SPEED: int = 4
```

#### 游戏机制配置
```python
ENEMY_SPAWN_RATE: float = 0.02
ENEMY_BULLET_RATE: float = 0.005
ENEMY_MEDIUM_BULLET_MULTIPLIER: float = 2.0
```

#### 音效配置
```python
SOUND_ENABLED: bool = True
SOUND_VOLUME: float = 0.5
SHOOT_SOUND_INTERVAL: int = 5
```

---

**文档版本**: 1.0.0  
**最后更新**: 2025-01-13
