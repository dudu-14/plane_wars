#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
道具系统模块
实现游戏中的各种道具类型和道具管理
"""

import pygame
import random
from typing import List, Tuple
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Item:
    """道具基类"""
    
    def __init__(self, x: float, y: float):
        """
        初始化道具
        
        Args:
            x: 道具x坐标
            y: 道具y坐标
        """
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 2
        self.active = True
        
    def update(self):
        """更新道具状态"""
        self.y += self.speed
        
        # 超出屏幕底部则销毁
        if self.y > SCREEN_HEIGHT:
            self.active = False
    
    def draw(self, screen):
        """绘制道具（子类需要重写）"""
        pass
    
    def get_rect(self):
        """获取道具的碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def apply_effect(self, player):
        """应用道具效果（子类需要重写）"""
        pass

class HealthItem(Item):
    """加血道具"""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.color = (0, 255, 0)  # 绿色
        
    def draw(self, screen):
        """绘制绿色十字"""
        # 绘制十字形状
        cross_size = 16
        cross_thickness = 4
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # 垂直线
        pygame.draw.rect(screen, self.color, 
                        (center_x - cross_thickness // 2, 
                         center_y - cross_size // 2,
                         cross_thickness, cross_size))
        
        # 水平线
        pygame.draw.rect(screen, self.color,
                        (center_x - cross_size // 2,
                         center_y - cross_thickness // 2,
                         cross_size, cross_thickness))
    
    def apply_effect(self, player):
        """增加玩家生命值"""
        if player.health < player.max_health:
            player.health += 1
            return True
        return False

class PowerUpItem(Item):
    """子弹强化道具"""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.color = (255, 255, 0)  # 黄色
        
    def draw(self, screen):
        """绘制黄色星形"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # 绘制星形（简化为菱形）
        points = [
            (center_x, center_y - 8),  # 上
            (center_x + 8, center_y),  # 右
            (center_x, center_y + 8),  # 下
            (center_x - 8, center_y)   # 左
        ]
        pygame.draw.polygon(screen, self.color, points)
        
        # 添加内部小菱形
        inner_points = [
            (center_x, center_y - 4),
            (center_x + 4, center_y),
            (center_x, center_y + 4),
            (center_x - 4, center_y)
        ]
        pygame.draw.polygon(screen, (255, 255, 255), inner_points)
    
    def apply_effect(self, player):
        """激活双发子弹效果"""
        player.activate_double_shot(10.0)  # 10秒双发效果
        return True

class ShieldItem(Item):
    """护盾道具"""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.color = (0, 100, 255)  # 蓝色
        
    def draw(self, screen):
        """绘制蓝色圆形护盾"""
        center_x = int(self.x + self.width // 2)
        center_y = int(self.y + self.height // 2)
        
        # 外圆
        pygame.draw.circle(screen, self.color, (center_x, center_y), 8)
        # 内圆
        pygame.draw.circle(screen, (150, 200, 255), (center_x, center_y), 5)
    
    def apply_effect(self, player):
        """激活护盾效果"""
        player.activate_shield(30.0)  # 30秒护盾效果
        return True

class ItemManager:
    """道具管理器"""
    
    def __init__(self):
        self.items: List[Item] = []
        
    def spawn_item(self, x: float, y: float, enemy_type: str = "small"):
        """
        生成道具
        
        Args:
            x: 生成位置x坐标
            y: 生成位置y坐标
            enemy_type: 敌机类型，影响道具掉落概率
        """
        # 添加随机偏移
        offset_x = random.randint(-20, 20)
        spawn_x = max(0, min(SCREEN_WIDTH - 20, x + offset_x))
        
        # 根据敌机类型和概率生成道具
        rand = random.random()
        
        if enemy_type == "medium":
            # 中型敌机掉落概率更高
            if rand < 0.15:  # 15% 加血道具
                self.items.append(HealthItem(spawn_x, y))
            elif rand < 0.35:  # 20% 子弹强化道具
                self.items.append(PowerUpItem(spawn_x, y))
            elif rand < 0.45:  # 10% 护盾道具
                self.items.append(ShieldItem(spawn_x, y))
        else:
            # 小型敌机掉落概率较低
            if rand < 0.05:  # 5% 加血道具
                self.items.append(HealthItem(spawn_x, y))
            elif rand < 0.25:  # 20% 子弹强化道具
                self.items.append(PowerUpItem(spawn_x, y))
            # 小型敌机不掉落护盾道具
    
    def update(self):
        """更新所有道具"""
        for item in self.items[:]:
            item.update()
            if not item.active:
                self.items.remove(item)
    
    def draw(self, screen):
        """绘制所有道具"""
        for item in self.items:
            item.draw(screen)
    
    def check_collision(self, player_rect) -> List[Item]:
        """
        检查与玩家的碰撞
        
        Args:
            player_rect: 玩家的碰撞矩形
            
        Returns:
            List[Item]: 碰撞的道具列表
        """
        collected_items = []
        for item in self.items[:]:
            if item.get_rect().colliderect(player_rect):
                collected_items.append(item)
                self.items.remove(item)
        return collected_items
    
    def clear(self):
        """清除所有道具"""
        self.items.clear()
