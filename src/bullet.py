#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""子弹模块。

本模块定义了子弹类，包含玩家子弹和敌机子弹的属性和行为。
子弹会自动移动，并在飞出屏幕时被自动清理。

典型用法示例:
    # 创建玩家子弹
    player_bullet = Bullet(x=400, y=300, bullet_type="player")

    # 创建敌机子弹
    enemy_bullet = Bullet(x=200, y=100, bullet_type="enemy")

    # 更新子弹位置
    player_bullet.update()
    enemy_bullet.update()

    # 绘制子弹
    player_bullet.draw(screen)
    enemy_bullet.draw(screen)
"""

import pygame
from typing import Literal, Tuple
from config import (
    BULLET_WIDTH, BULLET_HEIGHT, PLAYER_BULLET_SPEED, ENEMY_BULLET_SPEED,
    SCREEN_HEIGHT, YELLOW, RED
)

# 定义子弹类型的字面量类型
BulletType = Literal["player", "enemy"]


class Bullet:
    """子弹类。

    代表游戏中的子弹对象，支持玩家子弹和敌机子弹两种类型。
    不同类型的子弹具有不同的移动方向、速度和颜色。

    Attributes:
        x (int): 子弹的x坐标位置
        y (int): 子弹的y坐标位置
        width (int): 子弹的宽度
        height (int): 子弹的高度
        bullet_type (str): 子弹类型（"player" 或 "enemy"）
        speed (int): 子弹的移动速度（带方向）
        color (tuple): 子弹的颜色
        rect (pygame.Rect): 用于碰撞检测的矩形区域
    """

    def __init__(self, x: int, y: int, bullet_type: BulletType = "player") -> None:
        """初始化子弹。

        根据子弹类型设置相应的移动速度和颜色。
        玩家子弹向上移动，敌机子弹向下移动。

        Args:
            x (int): 子弹初始x坐标位置
            y (int): 子弹初始y坐标位置
            bullet_type (BulletType): 子弹类型，可选"player"或"enemy"
        """
        self.x: int = x
        self.y: int = y
        self.width: int = BULLET_WIDTH
        self.height: int = BULLET_HEIGHT
        self.bullet_type: BulletType = bullet_type

        # 根据子弹类型设置速度和颜色
        if bullet_type == "player":
            self.speed: int = -PLAYER_BULLET_SPEED  # 向上移动（负数）
            self.color: Tuple[int, int, int] = YELLOW
        else:  # enemy bullet
            self.speed = ENEMY_BULLET_SPEED   # 向下移动（正数）
            self.color = RED

        # 创建子弹矩形用于碰撞检测
        self.rect: pygame.Rect = pygame.Rect(x, y, self.width, self.height)

    def update(self) -> None:
        """更新子弹状态。

        让子弹沿着设定的方向移动，并更新碰撞检测矩形的位置。
        """
        self.y += self.speed

        # 更新碰撞检测矩形位置
        self.rect.x = self.x
        self.rect.y = self.y

    def is_off_screen(self) -> bool:
        """检查子弹是否已飞出屏幕。

        当子弹完全移出屏幕边界时，应该被移除以节省资源。
        检查上下两个边界，因为玩家子弹向上飞，敌机子弹向下飞。

        Returns:
            bool: 如果子弹已飞出屏幕返回True，否则返回False
        """
        return self.y < -self.height or self.y > SCREEN_HEIGHT

    def draw(self, screen: pygame.Surface) -> None:
        """绘制子弹。

        在屏幕上绘制子弹的图形表示。使用简单的矩形来表示子弹，
        不同类型的子弹使用不同的颜色。

        Args:
            screen (pygame.Surface): 要绘制到的屏幕表面
        """
        pygame.draw.rect(
            screen, self.color,
            (self.x, self.y, self.width, self.height)
        )
