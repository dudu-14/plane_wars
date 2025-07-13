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
        self.lives: int = PLAYER_INITIAL_LIVES
        self.last_bullet_time: float = 0.0

        # 创建飞机矩形用于碰撞检测
        self.rect: pygame.Rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, keys_pressed: pygame.key.ScancodeWrapper) -> None:
        """更新玩家飞机状态。

        根据键盘输入更新飞机位置，确保飞机不会移出屏幕边界。
        同时更新碰撞检测矩形的位置。

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

    def can_shoot(self) -> bool:
        """检查是否可以发射子弹。

        根据子弹冷却时间判断当前是否允许发射新的子弹。
        这个机制防止玩家无限制地快速发射子弹。

        Returns:
            bool: 如果可以发射子弹返回True，否则返回False
        """
        current_time: float = time.time()
        return current_time - self.last_bullet_time >= BULLET_COOLDOWN

    def shoot(self) -> Optional[Tuple[int, int]]:
        """发射子弹。

        如果满足发射条件，记录发射时间并返回子弹的初始位置。
        子弹从飞机的中心上方发射。

        Returns:
            Optional[Tuple[int, int]]: 如果可以发射，返回子弹初始位置(x, y)；
                                     否则返回None
        """
        if self.can_shoot():
            self.last_bullet_time = time.time()
            # 计算子弹的初始位置（飞机中心上方）
            bullet_x: int = self.x + self.width // 2 - BULLET_WIDTH // 2
            bullet_y: int = self.y
            return (bullet_x, bullet_y)
        return None

    def take_damage(self) -> None:
        """受到伤害。

        减少一点生命值。当生命值降到0时，玩家死亡。
        """
        self.lives -= 1

    def is_alive(self) -> bool:
        """检查玩家是否还活着。

        Returns:
            bool: 如果生命值大于0返回True，否则返回False
        """
        return self.lives > 0

    def draw(self, screen: pygame.Surface) -> None:
        """绘制玩家飞机。

        在屏幕上绘制玩家飞机的图形表示。使用简单的几何图形
        来表示飞机，包括主体和驾驶舱。

        Args:
            screen (pygame.Surface): 要绘制到的屏幕表面
        """
        # 绘制蓝色矩形代表玩家飞机主体
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

        # 绘制白色矩形代表飞机的驾驶舱
        cockpit_rect: pygame.Rect = pygame.Rect(
            self.x + 20, self.y + 10, 20, 30
        )
        pygame.draw.rect(screen, WHITE, cockpit_rect)
