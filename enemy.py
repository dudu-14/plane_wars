#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""敌机模块。

本模块定义了敌机类，包含不同类型敌机的属性、行为和绘制方法。
敌机会自动移动、发射子弹，并与玩家进行战斗。

典型用法示例:
    enemy = Enemy(x=100, y=0, enemy_type="small")
    enemy.update()
    bullet_pos = enemy.shoot()
    if bullet_pos:
        # 创建敌机子弹
        pass
    enemy.draw(screen)
"""

import pygame
import random
from typing import Optional, Tuple, Literal
from config import (
    ENEMY_SMALL_WIDTH, ENEMY_SMALL_HEIGHT, ENEMY_SMALL_SPEED,
    ENEMY_SMALL_HP, ENEMY_SMALL_SCORE,
    ENEMY_MEDIUM_WIDTH, ENEMY_MEDIUM_HEIGHT, ENEMY_MEDIUM_SPEED,
    ENEMY_MEDIUM_HP, ENEMY_MEDIUM_SCORE,
    BULLET_WIDTH, SCREEN_HEIGHT, ENEMY_BULLET_RATE,
    ENEMY_MEDIUM_BULLET_MULTIPLIER,
    RED, DARK_RED, GREEN, YELLOW
)

# 定义敌机类型的字面量类型
EnemyType = Literal["small", "medium"]


class Enemy:
    """敌机类。

    代表游戏中的敌方飞机，支持不同类型的敌机（小型和中型）。
    每种类型的敌机具有不同的属性，如大小、速度、生命值和分数。

    Attributes:
        enemy_type (str): 敌机类型（"small" 或 "medium"）
        x (int): 敌机的x坐标位置
        y (int): 敌机的y坐标位置
        width (int): 敌机的宽度
        height (int): 敌机的高度
        speed (int): 敌机的移动速度
        hp (int): 敌机当前生命值
        max_hp (int): 敌机最大生命值
        score (int): 击毁该敌机获得的分数
        color (tuple): 敌机的颜色
        rect (pygame.Rect): 用于碰撞检测的矩形区域
    """

    def __init__(self, x: int, y: int, enemy_type: EnemyType = "small") -> None:
        """初始化敌机。

        根据敌机类型设置相应的属性值，包括大小、速度、生命值等。

        Args:
            x (int): 敌机初始x坐标位置
            y (int): 敌机初始y坐标位置
            enemy_type (EnemyType): 敌机类型，可选"small"或"medium"
        """
        self.enemy_type: EnemyType = enemy_type
        self.x: int = x
        self.y: int = y

        # 根据敌机类型设置属性
        if enemy_type == "small":
            self.width: int = ENEMY_SMALL_WIDTH
            self.height: int = ENEMY_SMALL_HEIGHT
            self.speed: int = ENEMY_SMALL_SPEED
            self.hp: int = ENEMY_SMALL_HP
            self.max_hp: int = ENEMY_SMALL_HP
            self.score: int = ENEMY_SMALL_SCORE
            self.color: Tuple[int, int, int] = RED
        else:  # medium
            self.width = ENEMY_MEDIUM_WIDTH
            self.height = ENEMY_MEDIUM_HEIGHT
            self.speed = ENEMY_MEDIUM_SPEED
            self.hp = ENEMY_MEDIUM_HP
            self.max_hp = ENEMY_MEDIUM_HP
            self.score = ENEMY_MEDIUM_SCORE
            self.color = DARK_RED

        # 创建敌机矩形用于碰撞检测
        self.rect: pygame.Rect = pygame.Rect(x, y, self.width, self.height)

    def update(self) -> None:
        """更新敌机状态。

        让敌机向下移动，并更新碰撞检测矩形的位置。
        敌机以固定速度向屏幕下方移动。
        """
        # 向下移动
        self.y += self.speed

        # 更新碰撞检测矩形位置
        self.rect.x = self.x
        self.rect.y = self.y

    def is_off_screen(self) -> bool:
        """检查敌机是否已飞出屏幕。

        当敌机完全移出屏幕下边界时，应该被移除以节省资源。

        Returns:
            bool: 如果敌机已飞出屏幕返回True，否则返回False
        """
        return self.y > SCREEN_HEIGHT

    def can_shoot(self) -> bool:
        """检查敌机是否可以发射子弹。

        使用随机概率决定敌机是否发射子弹。中型敌机的发射概率
        比小型敌机更高，增加游戏难度。

        Returns:
            bool: 如果可以发射子弹返回True，否则返回False
        """
        base_rate: float = ENEMY_BULLET_RATE
        if self.enemy_type == "medium":
            # 中型敌机发射概率更高
            return random.random() < base_rate * ENEMY_MEDIUM_BULLET_MULTIPLIER
        else:
            return random.random() < base_rate

    def shoot(self) -> Optional[Tuple[int, int]]:
        """发射子弹。

        如果满足发射条件，返回子弹的初始位置。
        子弹从敌机的中心下方发射。

        Returns:
            Optional[Tuple[int, int]]: 如果可以发射，返回子弹初始位置(x, y)；
                                     否则返回None
        """
        if self.can_shoot():
            # 计算子弹的初始位置（敌机中心下方）
            bullet_x: int = self.x + self.width // 2 - BULLET_WIDTH // 2
            bullet_y: int = self.y + self.height
            return (bullet_x, bullet_y)
        return None

    def take_damage(self) -> None:
        """受到伤害。

        减少一点生命值。当生命值降到0时，敌机被摧毁。
        """
        self.hp -= 1

    def is_alive(self) -> bool:
        """检查敌机是否还活着。

        Returns:
            bool: 如果生命值大于0返回True，否则返回False
        """
        return self.hp > 0

    def draw(self, screen: pygame.Surface) -> None:
        """绘制敌机。

        在屏幕上绘制敌机的图形表示，包括主体、血量条（如果受伤）和武器。
        不同类型的敌机使用不同的颜色来区分。

        Args:
            screen (pygame.Surface): 要绘制到的屏幕表面
        """
        # 绘制敌机主体
        pygame.draw.rect(
            screen, self.color,
            (self.x, self.y, self.width, self.height)
        )

        # 绘制血量条（仅在受伤时显示）
        if self.hp < self.max_hp:
            self._draw_health_bar(screen)

        # 绘制敌机的武器系统
        self._draw_weapon(screen)

    def _draw_health_bar(self, screen: pygame.Surface) -> None:
        """绘制敌机的血量条。

        在敌机上方显示血量条，红色背景表示最大血量，
        绿色前景表示当前血量。

        Args:
            screen (pygame.Surface): 要绘制到的屏幕表面
        """
        bar_width: int = self.width
        bar_height: int = 4
        bar_x: int = self.x
        bar_y: int = self.y - 8

        # 绘制血量条背景（红色）
        pygame.draw.rect(
            screen, RED,
            (bar_x, bar_y, bar_width, bar_height)
        )

        # 绘制当前血量（绿色）
        current_width: int = int(bar_width * (self.hp / self.max_hp))
        pygame.draw.rect(
            screen, GREEN,
            (bar_x, bar_y, current_width, bar_height)
        )

    def _draw_weapon(self, screen: pygame.Surface) -> None:
        """绘制敌机的武器系统。

        在敌机底部中央绘制一个小的黄色矩形，代表武器。

        Args:
            screen (pygame.Surface): 要绘制到的屏幕表面
        """
        weapon_rect: pygame.Rect = pygame.Rect(
            self.x + self.width // 2 - 2,  # 武器x坐标（居中）
            self.y + self.height - 5,      # 武器y坐标（底部）
            4,                             # 武器宽度
            8                              # 武器高度
        )
        pygame.draw.rect(screen, YELLOW, weapon_rect)
