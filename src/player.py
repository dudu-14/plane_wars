#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""玩家飞机模块。

本模块定义了玩家控制的飞机类，包含飞机的移动、射击、碰撞检测等功能。
玩家飞机是游戏的核心对象，负责响应用户输入并与游戏世界交互。

典型用法示例:
    player = Player(x=400, y=500)
    player.update(keys_pressed)
    bullet_pos = player.shoot()
    if bullet_pos:
        # 创建子弹对象
        pass
"""

import pygame
import time
from typing import Optional, Tuple
from config import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_INITIAL_LIVES,
    BULLET_COOLDOWN, BULLET_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT,
    BLUE, WHITE
)


class Player:
    """玩家飞机类。

    代表玩家控制的飞机，具有移动、射击、受伤等功能。
    飞机的位置、状态和行为都由这个类管理。

    Attributes:
        x (int): 飞机的x坐标位置
        y (int): 飞机的y坐标位置
        width (int): 飞机的宽度
        height (int): 飞机的高度
        speed (int): 飞机的移动速度
        lives (int): 飞机的剩余生命值
        last_bullet_time (float): 上次发射子弹的时间戳
        rect (pygame.Rect): 用于碰撞检测的矩形区域
    """

    def __init__(self, x: int, y: int) -> None:
        """初始化玩家飞机。

        Args:
            x (int): 飞机初始x坐标位置
            y (int): 飞机初始y坐标位置
        """
        self.x: int = x
        self.y: int = y
        self.width: int = PLAYER_WIDTH
        self.height: int = PLAYER_HEIGHT
        self.speed: int = PLAYER_SPEED

        # 生命值系统 - 1.1.0新增
        self.health: int = 3  # 当前生命值
        self.max_health: int = 5  # 最大生命值上限
        self.lives: int = PLAYER_INITIAL_LIVES  # 保持兼容性

        # 射击系统
        self.last_bullet_time: float = 0.0

        # 道具效果系统 - 1.1.0新增
        self.double_shot_active: bool = False
        self.double_shot_end_time: float = 0.0
        self.shield_active: bool = False
        self.shield_end_time: float = 0.0

        # 创建飞机矩形用于碰撞检测
        self.rect: pygame.Rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, keys_pressed: pygame.key.ScancodeWrapper) -> None:
        """更新玩家飞机状态。

        根据键盘输入更新飞机位置，确保飞机不会移出屏幕边界。
        同时更新碰撞检测矩形的位置和道具效果状态。

        Args:
            keys_pressed (pygame.key.ScancodeWrapper): 当前按下的键盘按键状态
        """
        # 处理左右移动
        if keys_pressed[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

        # 处理上下移动
        if keys_pressed[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys_pressed[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed

        # 更新碰撞检测矩形位置
        self.rect.x = self.x
        self.rect.y = self.y

        # 更新道具效果状态 - 1.1.0新增
        current_time = time.time()

        # 检查双发子弹效果是否过期
        if self.double_shot_active and current_time >= self.double_shot_end_time:
            self.double_shot_active = False

        # 检查护盾效果是否过期
        if self.shield_active and current_time >= self.shield_end_time:
            self.shield_active = False

    def can_shoot(self) -> bool:
        """检查是否可以发射子弹。

        根据子弹冷却时间判断当前是否允许发射新的子弹。
        这个机制防止玩家无限制地快速发射子弹。

        Returns:
            bool: 如果可以发射子弹返回True，否则返回False
        """
        current_time: float = time.time()
        return current_time - self.last_bullet_time >= BULLET_COOLDOWN

    def shoot(self) -> Optional[list]:
        """发射子弹。

        如果满足发射条件，记录发射时间并返回子弹的初始位置。
        支持双发子弹模式（道具效果激活时）。

        Returns:
            Optional[list]: 如果可以发射，返回子弹初始位置列表[(x, y), ...]；
                           否则返回None
        """
        if self.can_shoot():
            self.last_bullet_time = time.time()
            bullets = []

            if self.double_shot_active:
                # 双发子弹模式 - 1.1.0新增
                left_bullet_x = self.x + self.width // 2 - 15 - BULLET_WIDTH // 2
                right_bullet_x = self.x + self.width // 2 + 15 - BULLET_WIDTH // 2
                bullet_y = self.y

                bullets.append((left_bullet_x, bullet_y))
                bullets.append((right_bullet_x, bullet_y))
            else:
                # 单发子弹模式
                bullet_x = self.x + self.width // 2 - BULLET_WIDTH // 2
                bullet_y = self.y
                bullets.append((bullet_x, bullet_y))

            return bullets
        return None

    def take_damage(self) -> bool:
        """受到伤害。

        优先消耗护盾，护盾消失后才减少生命值。

        Returns:
            bool: 如果实际受到伤害返回True，护盾抵挡返回False
        """
        if self.shield_active:
            # 护盾抵挡伤害 - 1.1.0新增
            self.shield_active = False
            return False
        else:
            # 减少生命值
            self.health -= 1
            self.lives -= 1  # 保持兼容性
            return True

    def is_alive(self) -> bool:
        """检查玩家是否还活着。

        Returns:
            bool: 如果生命值大于0返回True，否则返回False
        """
        return self.health > 0 and self.lives > 0

    def draw(self, screen: pygame.Surface) -> None:
        """绘制玩家飞机。

        在屏幕上绘制玩家飞机的图形表示。使用简单的几何图形
        来表示飞机，包括主体和驾驶舱。

        Args:
            screen (pygame.Surface): 要绘制到的屏幕表面
        """
        # 绘制蓝色矩形代表玩家飞机主体
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

        # 绘制护盾效果 - 1.1.0新增
        if self.shield_active:
            pygame.draw.circle(screen, (0, 150, 255),
                             (self.x + self.width // 2, self.y + self.height // 2),
                             max(self.width, self.height) // 2 + 5, 2)

        # 绘制白色矩形代表飞机的驾驶舱
        cockpit_rect: pygame.Rect = pygame.Rect(
            self.x + 20, self.y + 10, 20, 30
        )
        pygame.draw.rect(screen, WHITE, cockpit_rect)

    # 道具效果激活方法 - 1.1.0新增
    def activate_double_shot(self, duration: float) -> None:
        """激活双发子弹效果

        Args:
            duration: 效果持续时间（秒）
        """
        self.double_shot_active = True
        self.double_shot_end_time = time.time() + duration

    def activate_shield(self, duration: float) -> None:
        """激活护盾效果

        Args:
            duration: 效果持续时间（秒）
        """
        self.shield_active = True
        self.shield_end_time = time.time() + duration

    def get_power_up_status(self) -> dict:
        """获取当前道具效果状态

        Returns:
            dict: 包含各种道具效果状态和剩余时间的字典
        """
        current_time = time.time()
        return {
            'double_shot': {
                'active': self.double_shot_active,
                'remaining': max(0, self.double_shot_end_time - current_time) if self.double_shot_active else 0
            },
            'shield': {
                'active': self.shield_active,
                'remaining': max(0, self.shield_end_time - current_time) if self.shield_active else 0
            },
            'health': self.health,
            'max_health': self.max_health
        }
